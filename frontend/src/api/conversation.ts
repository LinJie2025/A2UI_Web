import client from "./client";
import type { ApiResponse } from "@/types";

export interface ConversationSummary {
  id: number;
  user_id: number;
  title: string | null;
  created_at: string;
  updated_at: string;
  message_count: number;
  last_message: string | null;
}

export interface ConversationMessage {
  id: number;
  conversation_id: number;
  role: string;
  content: string | null;
  tool_calls_json: string | null;
  tool_call_id: string | null;
  created_at: string;
}

export interface ConversationDetail extends ConversationSummary {
  messages: ConversationMessage[];
}

export async function getConversationsApi(): Promise<ApiResponse<ConversationSummary[]>> {
  const resp = await client.get<ApiResponse<ConversationSummary[]>>("/conversations");
  return resp.data;
}

export async function getConversationApi(id: number): Promise<ApiResponse<ConversationDetail>> {
  const resp = await client.get<ApiResponse<ConversationDetail>>(`/conversations/${id}`);
  return resp.data;
}

export async function getConversationMessagesApi(id: number): Promise<ApiResponse<ConversationMessage[]>> {
  const resp = await client.get<ApiResponse<ConversationMessage[]>>(`/conversations/${id}/messages`);
  return resp.data;
}

export async function deleteConversationApi(id: number): Promise<ApiResponse<null>> {
  const resp = await client.delete<ApiResponse<null>>(`/conversations/${id}`);
  return resp.data;
}
