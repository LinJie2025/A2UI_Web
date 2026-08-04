/** A2UI Action types — matches backend schemas/a2ui_action.py */

/** Request body for POST /api/a2ui/submit */
export interface A2UIActionSubmitRequest {
  conversation_id: number;
  action_name: string;
  form_data: Record<string, unknown>;
}

/** A single A2UI action record */
export interface A2UIAction {
  id: number;
  conversation_id: number;
  action_name: string;
  form_data: Record<string, unknown> | null;
  status: "submitted" | "processing" | "done" | "failed" | "interrupted";
  result_summary: string | null;
  error_detail: string | null;
  tool_call_id: string | null;
  created_at: string;
  updated_at: string;
}
