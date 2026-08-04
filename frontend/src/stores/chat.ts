import { defineStore } from "pinia";
import { ref, computed } from "vue";
import type { ChatMessage, StreamingMessage } from "@/types/chat";

/** A single step in the A2UI overlay */
export interface A2UIOverlayStep {
  id: string;
  title: string;
  content: string;
  status: "pending" | "active" | "done";
}

export const useChatStore = defineStore("chat", () => {
  const messages = ref<ChatMessage[]>([]);
  const currentStreamingMessage = ref<StreamingMessage | null>(null);
  const isStreaming = ref(false);

  // Overlay
  const showA2UIOverlay = ref(false);
  const a2uiOverlaySteps = ref<A2UIOverlayStep[]>([]);
  const currentStepIndex = ref(0);
  const totalSteps = computed(() => a2uiOverlaySteps.value.length);
  const hasNextStep = computed(() => currentStepIndex.value < totalSteps.value - 1);
  const hasPrevStep = computed(() => currentStepIndex.value > 0);
  const isLastStep = computed(() => currentStepIndex.value === totalSteps.value - 1);
  const currentStepContent = computed(() => {
    return a2uiOverlaySteps.value[currentStepIndex.value]?.content ?? "";
  });
  const overlayBadge = computed(() => {
    if (totalSteps.value === 0) return "";
    if (isLastStep.value) return "done";
    return "active";
  });

  function openA2UIOverlay(rawText: string, title?: string) {
    if (a2uiOverlaySteps.value.length > 0) {
      showA2UIOverlay.value = true;
      return;
    }
    const extractedTitle = title || extractTitleFromContent(rawText) || "Step 1";
    a2uiOverlaySteps.value = [
      {
        id: `step_${Date.now()}`,
        title: extractedTitle,
        content: rawText,
        status: totalSteps.value > 1 ? "done" : "active",
      },
    ];
    currentStepIndex.value = 0;
    showA2UIOverlay.value = true;
  }

  function addOverlayStep(rawText: string, title?: string) {
    const extractedTitle = title || extractTitleFromContent(rawText) || `Step ${a2uiOverlaySteps.value.length + 1}`;
    a2uiOverlaySteps.value.forEach((s) => {
      if (s.status === "active") s.status = "done";
    });
    a2uiOverlaySteps.value.push({
      id: `step_${Date.now()}`,
      title: extractedTitle,
      content: rawText,
      status: "active",
    });
    currentStepIndex.value = a2uiOverlaySteps.value.length - 1;
  }

  function goToStep(index: number) {
    if (index >= 0 && index < a2uiOverlaySteps.value.length) {
      currentStepIndex.value = index;
    }
  }

  function prevStep() { if (hasPrevStep.value) currentStepIndex.value--; }
  function nextStep() { if (hasNextStep.value) currentStepIndex.value++; }

  function closeA2UIOverlay() {
    showA2UIOverlay.value = false;
  }

  function extractTitleFromContent(text: string): string | null {
    if (!text) return null;
    try {
      const lines = text.split("\n");
      for (const line of lines) {
        const trimmed = line.trim();
        if (!trimmed) continue;
        const parsed = JSON.parse(trimmed);
        if (parsed.updateComponents) {
          const comps = parsed.updateComponents.components;
          if (Array.isArray(comps)) {
            for (const comp of comps) {
              if (comp.component === "Text" && comp.text && typeof comp.text === "string") {
                return comp.text;
              }
            }
          }
        }
      }
    } catch { /* not valid JSON */ }
    return null;
  }

  function addMessage(msg: ChatMessage) { messages.value.push(msg); }
  function setMessages(msgs: ChatMessage[]) { messages.value = msgs; }

  function updateMessageContent(index: number, content: string) {
    if (index >= 0 && index < messages.value.length) {
      messages.value[index] = {
        ...messages.value[index],
        content: (messages.value[index].content || "") + "\n" + content,
      };
    }
  }

  function setStreamingMessage(msg: StreamingMessage | null) { currentStreamingMessage.value = msg; }
  function setStreaming(active: boolean) { isStreaming.value = active; }

  function clearMessages() {
    messages.value = [];
    currentStreamingMessage.value = null;
    a2uiOverlaySteps.value = [];
    currentStepIndex.value = 0;
    showA2UIOverlay.value = false;
  }

  return {
    messages, currentStreamingMessage, isStreaming,
    showA2UIOverlay, a2uiOverlaySteps, currentStepIndex,
    totalSteps, hasNextStep, hasPrevStep, isLastStep,
    currentStepContent, overlayBadge,
    openA2UIOverlay, addOverlayStep, goToStep, prevStep, nextStep, closeA2UIOverlay,
    addMessage, setMessages, updateMessageContent, setStreamingMessage, setStreaming, clearMessages,
  };
});
