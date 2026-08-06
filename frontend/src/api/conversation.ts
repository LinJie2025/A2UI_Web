import client from "./client";
import type { ApiResponse } from "@/types";
import type { Message } from "@/types/chat";

export interface ConversationSummary {
  id: number;
  user_id: number;
  title: string | null;
  created_at: string;
  updated_at: string;
  message_count: number;
  last_message: string | null;
}

export interface ConversationDetail extends ConversationSummary {
  messages: Message[];
}

/** List all conversations for current user. */
export async function getConversationsApi(): Promise<ApiResponse<ConversationSummary[]>> {
  const resp = await client.get<ApiResponse<ConversationSummary[]>>("/conversations");
  return resp.data;
}

/** Get conversation detail with all messages. */
export async function getConversationApi(id: number): Promise<ApiResponse<ConversationDetail>> {
  const resp = await client.get<ApiResponse<ConversationDetail>>(`/conversations/${id}`);
  return resp.data;
}

/** Update conversation title. */
export async function updateConversationApi(
  id: number,
  title: string,
): Promise<ApiResponse<ConversationSummary>> {
  const resp = await client.put<ApiResponse<ConversationSummary>>(`/conversations/${id}`, { title });
  return resp.data;
}

/** Delete a conversation. */
export async function deleteConversationApi(id: number): Promise<ApiResponse<null>> {
  const resp = await client.delete<ApiResponse<null>>(`/conversations/${id}`);
  return resp.data;
}
