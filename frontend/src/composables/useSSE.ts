/** Composable for SSE streaming — fetch() + ReadableStream + TextDecoderStream. */

import { ref, type Ref } from "vue";
import { SSEParser } from "@/utils/sse-parser";
import type { ParsedSSEEvent, StreamingMessage, ToolCallStatus } from "@/types/chat";
import { useAuthStore } from "@/stores/auth";

export interface UseSSEReturn {
  /** Whether the stream is currently active. */
  isStreaming: Ref<boolean>;
  /** The streaming assistant message being built. */
  streamingMessage: Ref<StreamingMessage | null>;
  /** Error message if the stream failed. */
  error: Ref<string | null>;
  /** Start a new SSE stream. */
  startStream: (body: object, url?: string) => Promise<void>;
  /** Abort the current stream. */
  abort: () => void;
}

export function useSSE(): UseSSEReturn {
  const isStreaming = ref(false);
  const streamingMessage = ref<StreamingMessage | null>(null);
  const error = ref<string | null>(null);
  let abortController: AbortController | null = null;

  function resetStreamingMessage(): StreamingMessage {
    return {
      id: `msg_${Date.now()}`,
      role: "assistant",
      content: "",
      toolCalls: [],
      isComplete: false,
      conversationId: null,
    };
  }

  function handleEvent(event: ParsedSSEEvent): void {
    if (!streamingMessage.value) return;

    switch (event.event) {
      case "user_message_saved": {
        // Capture conversation_id from the initial event
        if (event.data.conversation_id) {
          streamingMessage.value.conversationId = event.data.conversation_id as number;
        }
        break;
      }
      case "text": {
        const delta = (event.data.delta as string) || "";
        streamingMessage.value.content += delta;
        break;
      }
      case "tool_call": {
        const tc: ToolCallStatus = {
          id: (event.data.id as string) || "",
          name: (event.data.name as string) || "",
          arguments: (event.data.arguments as Record<string, unknown>) || {},
          status: "running",
        };
        streamingMessage.value.toolCalls.push(tc);
        break;
      }
      case "tool_result": {
        const id = (event.data.id as string) || "";
        const tool = streamingMessage.value.toolCalls.find((t) => t.id === id);
        if (tool) {
          tool.status = "success";
          tool.result = event.data.result;
        }
        break;
      }
      case "error": {
        const msg = (event.data.message as string) || "Unknown error";
        error.value = msg;
        break;
      }
      case "done": {
        streamingMessage.value.isComplete = true;
        isStreaming.value = false;
        // Capture conversation_id from done event (set by both /api/chat and /api/a2ui/submit)
        if (event.data.conversation_id) {
          streamingMessage.value.conversationId = event.data.conversation_id as number;
        }
        break;
      }
    }
  }

  async function startStream(body: object, url: string = "/api/chat"): Promise<void> {
    const authStore = useAuthStore();
    if (!authStore.token) {
      error.value = "Not authenticated.";
      return;
    }

    abortController = new AbortController();
    isStreaming.value = true;
    error.value = null;
    streamingMessage.value = resetStreamingMessage();

    const parser = new SSEParser(handleEvent);

    try {
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${authStore.token}`,
        },
        body: JSON.stringify(body),
        signal: abortController.signal,
      });

      if (!response.ok) {
        const errData = await response.json().catch(() => ({}));
        throw new Error(
          (errData as { detail?: { message?: string } })?.detail?.message ||
            `HTTP ${response.status}`
        );
      }

      if (!response.body) {
        throw new Error("Response body is null.");
      }

      const reader = response.body
        .pipeThrough(new TextDecoderStream())
        .getReader();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        parser.feed(value);
      }

      parser.flush();
    } catch (e: unknown) {
      if ((e as Error).name === "AbortError") {
        // User cancelled
      } else {
        error.value = (e as Error).message || "Stream failed.";
      }
    } finally {
      isStreaming.value = false;
      if (streamingMessage.value) {
        streamingMessage.value.isComplete = true;
      }
    }
  }

  function abort(): void {
    if (abortController) {
      abortController.abort();
      abortController = null;
    }
  }

  return {
    isStreaming,
    streamingMessage,
    error,
    startStream,
    abort,
  };
}
