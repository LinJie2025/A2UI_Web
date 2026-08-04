import client from "./client";
import type { ApiResponse } from "@/types";
import type { A2UIAction } from "@/types/action";

/** Get all A2UI actions for a conversation */
export async function getConversationActionsApi(
  conversationId: number
): Promise<ApiResponse<A2UIAction[]>> {
  const resp = await client.get<ApiResponse<A2UIAction[]>>(
    `/conversations/${conversationId}/actions`
  );
  return resp.data;
}
