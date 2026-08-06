/** Chat request builder — v2 unified format.

SSE streaming uses native fetch() in useSSE composable, not axios.
This file provides typed helpers for building the request payload.
*/

import type { ChatRequest } from "@/types/chat";

/**
 * Build a chat request for normal text conversation.
 */
export function buildChatRequest(
  content: string,
  conversationId: number | null = null,
): ChatRequest {
  return {
    conversation_id: conversationId,
    message: {
      role: "user",
      content,
    },
  };
}

/**
 * Build a chat request for A2UI form submission.
 */
export function buildActionRequest(
  actionName: string,
  formData: Record<string, unknown>,
  conversationId: number,
): ChatRequest {
  return {
    conversation_id: conversationId,
    message: {
      role: "user",
      content: null,
      meta: {
        action_name: actionName,
        form_data: formData,
      },
    },
  };
}
