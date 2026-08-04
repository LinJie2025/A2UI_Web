/** SSE parser utilities — parse raw SSE text stream into typed events. */

import type { ParsedSSEEvent, SSEEventType } from "@/types/chat";

const VALID_EVENTS: Set<string> = new Set([
  "text",
  "tool_call",
  "tool_result",
  "done",
  "error",
]);

/**
 * Parse a raw SSE text chunk and emit parsed events via callback.
 *
 * The parser handles partial chunks — incomplete events are buffered and
 * emitted once the double-newline terminator is received.
 */
export class SSEParser {
  private buffer = "";
  private onEvent: (event: ParsedSSEEvent) => void;

  constructor(onEvent: (event: ParsedSSEEvent) => void) {
    this.onEvent = onEvent;
  }

  /** Feed raw text data into the parser. */
  feed(chunk: string): void {
    this.buffer += chunk;

    // Process complete events (terminated by \n\n)
    while (true) {
      const idx = this.buffer.indexOf("\n\n");
      if (idx === -1) break;

      const raw = this.buffer.slice(0, idx);
      this.buffer = this.buffer.slice(idx + 2);
      this._parseEvent(raw);
    }
  }

  /** Flush remaining buffer (called when stream ends). */
  flush(): void {
    if (this.buffer.trim()) {
      this._parseEvent(this.buffer);
      this.buffer = "";
    }
  }

  /** Parse a single SSE event block. */
  private _parseEvent(raw: string): void {
    const lines = raw.split("\n");
    let eventType: SSEEventType = "text";
    let dataStr = "";

    for (const line of lines) {
      if (line.startsWith("event: ")) {
        const type = line.slice(7).trim();
        if (VALID_EVENTS.has(type)) {
          eventType = type as SSEEventType;
        }
      } else if (line.startsWith("data: ")) {
        dataStr = line.slice(6).trim();
      }
    }

    if (!dataStr) return;

    try {
      const data = JSON.parse(dataStr) as Record<string, unknown>;
      this.onEvent({ event: eventType, data });
    } catch {
      // If data is not valid JSON, treat as text
      this.onEvent({
        event: "text",
        data: { delta: dataStr },
      });
    }
  }
}
