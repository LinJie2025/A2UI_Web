/** A2UI Protocol JSONL Parser

Parses raw text (LLM output) that may contain A2UI protocol messages
interleaved with plain text. Builds surface states from the stream of messages.

Protocol flow:
  createSurface → updateComponents → updateDataModel → [deleteSurface]
*/

import type {
  A2UIMessage,
  ComponentDef,
  ParsedA2UILine,
  ParsedA2UIResult,
  SurfaceState,
} from "@/types/a2ui";

// ─── Message Detection ────────────────────────────────────────────────────

const MESSAGE_KEYS = new Set([
  "createSurface",
  "updateComponents",
  "updateDataModel",
  "deleteSurface",
]);

function isA2UIMessage(obj: unknown): obj is A2UIMessage {
  if (!obj || typeof obj !== "object") return false;
  const keys = Object.keys(obj as Record<string, unknown>);
  // An A2UI message has exactly one top-level key, and it must be a known message type
  if (keys.length !== 1) return false;
  const key = keys[0];
  if (!MESSAGE_KEYS.has(key)) return false;

  // Validate the inner structure has required fields
  const inner = (obj as Record<string, unknown>)[key] as Record<string, unknown>;
  if (!inner || typeof inner !== "object") return false;

  switch (key) {
    case "createSurface":
      return typeof inner.surfaceId === "string";
    case "updateComponents":
      return typeof inner.surfaceId === "string" && Array.isArray(inner.components);
    case "updateDataModel":
      return typeof inner.surfaceId === "string";
    case "deleteSurface":
      return typeof inner.surfaceId === "string";
    default:
      return false;
  }
}

// ─── JSON Pointer Resolution ──────────────────────────────────────────────

/**
 * Resolve a JSON Pointer path against a data model.
 * Supports only simple paths like "/contacts/0/name".
 */
function resolveJsonPointer(
  model: Record<string, unknown>,
  path: string,
): unknown {
  if (path === "/" || path === "") return model;

  const segments = path.startsWith("/")
    ? path.slice(1).split("/")
    : path.split("/");

  let current: unknown = model;
  for (const seg of segments) {
    if (seg === "") continue;
    if (current === null || current === undefined) return undefined;
    if (typeof current !== "object") return undefined;

    const obj = current as Record<string, unknown>;
    // Try numeric index for arrays
    if (/^\d+$/.test(seg) && Array.isArray(obj)) {
      current = (obj as unknown[])[parseInt(seg, 10)];
    } else {
      current = obj[seg];
    }
  }
  return current;
}

// ─── Surface State Builder ─────────────────────────────────────────────────

/**
 * Process a sequence of A2UI messages to build surface states.
 * Handles createSurface, updateComponents (add/update), updateDataModel (merge), deleteSurface.
 */
export function buildSurfaces(messages: A2UIMessage[]): Map<string, SurfaceState> {
  const surfaces = new Map<string, SurfaceState>();

  for (const msg of messages) {
    if ("createSurface" in msg) {
      const { surfaceId, catalogId } = msg.createSurface;
      surfaces.set(surfaceId, {
        surfaceId,
        catalogId,
        components: new Map(),
        dataModel: {},
        rootId: "root",
      });
    } else if ("updateComponents" in msg) {
      const { surfaceId, components } = msg.updateComponents;
      let surface = surfaces.get(surfaceId);
      // Auto-create surface if not yet created (tolerant mode)
      if (!surface) {
        surface = {
          surfaceId,
          catalogId: "basic",
          components: new Map(),
          dataModel: {},
          rootId: "root",
        };
        surfaces.set(surfaceId, surface);
      }
      for (const comp of components) {
        surface.components.set(comp.id, comp);
      }
    } else if ("updateDataModel" in msg) {
      const { surfaceId, path, value } = msg.updateDataModel;
      let surface = surfaces.get(surfaceId);
      if (!surface) {
        surface = {
          surfaceId,
          catalogId: "basic",
          components: new Map(),
          dataModel: {},
          rootId: "root",
        };
        surfaces.set(surfaceId, surface);
      }

      if (value === undefined && path) {
        // Delete key at path
        deleteAtPath(surface.dataModel, path);
      } else if (path && path !== "/") {
        // Set value at specific path
        setAtPath(surface.dataModel, path, value);
      } else {
        // Replace entire data model
        surface.dataModel = (value as Record<string, unknown>) || {};
      }
    } else if ("deleteSurface" in msg) {
      surfaces.delete(msg.deleteSurface.surfaceId);
    }
  }

  return surfaces;
}

function setAtPath(obj: Record<string, unknown>, path: string, value: unknown): void {
  const segments = path.startsWith("/") ? path.slice(1).split("/") : path.split("/");
  let current: Record<string, unknown> = obj;
  for (let i = 0; i < segments.length - 1; i++) {
    const seg = segments[i];
    if (!seg) continue;
    if (!(seg in current) || typeof current[seg] !== "object" || current[seg] === null) {
      current[seg] = {};
    }
    current = current[seg] as Record<string, unknown>;
  }
  const lastSeg = segments[segments.length - 1];
  if (lastSeg) {
    current[lastSeg] = value;
  }
}

function deleteAtPath(obj: Record<string, unknown>, path: string): void {
  const segments = path.startsWith("/") ? path.slice(1).split("/") : path.split("/");
  let current: Record<string, unknown> = obj;
  for (let i = 0; i < segments.length - 1; i++) {
    const seg = segments[i];
    if (!seg || !(seg in current)) return;
    current = current[seg] as Record<string, unknown>;
  }
  const lastSeg = segments[segments.length - 1];
  if (lastSeg) {
    delete current[lastSeg];
  }
}

// ─── Render Tree Builder ───────────────────────────────────────────────────

import type { RenderNode } from "@/types/a2ui";

/**
 * Build a render tree from a surface state.
 * Resolves data bindings and assembles the component tree from the adjacency list.
 */
export function buildRenderTree(surface: SurfaceState): RenderNode | null {
  return buildNode(surface.rootId, surface);
}

function buildNode(
  componentId: string,
  surface: SurfaceState,
): RenderNode | null {
  const def = surface.components.get(componentId);
  if (!def) return null;

  // Resolve children
  const childIds = getChildIds(def);
  const children: RenderNode[] = [];
  for (const childId of childIds) {
    const childNode = buildNode(childId, surface);
    if (childNode) children.push(childNode);
  }

  // Resolve props with data binding
  const props = resolveProps(def, surface.dataModel);

  return {
    id: def.id,
    component: def.component,
    props,
    children,
  };
}

function getChildIds(def: ComponentDef): string[] {
  // "children" field (Column, Row, List)
  if (Array.isArray(def.children)) {
    return def.children.filter((c): c is string => typeof c === "string");
  }
  // "child" field (Card, Button)
  if (typeof def.child === "string") {
    return [def.child];
  }
  return [];
}

function resolveProps(
  def: ComponentDef,
  dataModel: Record<string, unknown>,
): Record<string, unknown> {
  const resolved: Record<string, unknown> = {};

  for (const [key, value] of Object.entries(def)) {
    // Skip internal keys
    if (key === "id" || key === "component" || key === "children" || key === "child") {
      continue;
    }
    resolved[key] = resolveValue(value, dataModel);
  }

  return resolved;
}

function resolveValue(value: unknown, dataModel: Record<string, unknown>): unknown {
  if (value === null || value === undefined) return value;

  // Check if it's a DataPath object { path: "..." }
  if (
    typeof value === "object" &&
    !Array.isArray(value) &&
    "path" in value &&
    typeof (value as Record<string, unknown>).path === "string"
  ) {
    return resolveJsonPointer(dataModel, (value as { path: string }).path);
  }

  // Recurse into objects and arrays
  if (Array.isArray(value)) {
    return value.map((v) => resolveValue(v, dataModel));
  }

  if (typeof value === "object") {
    const resolved: Record<string, unknown> = {};
    for (const [k, v] of Object.entries(value as Record<string, unknown>)) {
      resolved[k] = resolveValue(v, dataModel);
    }
    return resolved;
  }

  return value;
}

// ─── Main Parse Function ──────────────────────────────────────────────────

/**
 * Parse raw LLM output text into A2UI lines.
 * Each line is tried as JSON first; A2UI messages are extracted, rest becomes text.
 */
export function parseA2UI(text: string): ParsedA2UIResult {
  const result: ParsedA2UIResult = {
    textLines: [],
    messages: [],
    surfaces: new Map(),
    errors: [],
  };

  if (!text) return result;

  const lines = text.split("\n");

  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed) continue;

    try {
      const parsed = JSON.parse(trimmed);
      if (isA2UIMessage(parsed)) {
        result.messages.push(parsed);
        continue;
      }
      // Valid JSON but not an A2UI message — treat as text
      result.textLines.push(trimmed);
    } catch {
      // Not valid JSON — plain text
      result.textLines.push(trimmed);
    }
  }

  // Build surface states from accumulated messages
  result.surfaces = buildSurfaces(result.messages);

  return result;
}

/**
 * Quick check: does this text contain any A2UI messages?
 * Used by ChatMessage to decide rendering mode.
 */
export function hasA2UIMessages(text: string): boolean {
  if (!text) return false;
  const lines = text.split("\n");
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed) continue;
    try {
      const parsed = JSON.parse(trimmed);
      if (isA2UIMessage(parsed)) return true;
    } catch {
      // continue
    }
  }
  return false;
}
