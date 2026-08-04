/** A2UI Protocol v0.9.1 — Type Definitions

Matches the real A2UI protocol specification:
https://a2ui.org/specification/v0.9.1-a2ui/

Message types: createSurface → updateComponents → updateDataModel → deleteSurface
*/

// ─── Envelope (each JSONL line) ───────────────────────────────────────────

export interface CreateSurface {
  surfaceId: string;
  catalogId: string;
}

export interface UpdateComponents {
  surfaceId: string;
  components: ComponentDef[];
}

export interface UpdateDataModel {
  surfaceId: string;
  /** JSON Pointer path, e.g. "/contacts" or "/contact/name". Default "/". */
  path?: string;
  /** The data value. If omitted, deletes the key at path. */
  value?: unknown;
}

export interface DeleteSurface {
  surfaceId: string;
}

/** Top-level A2UI message — exactly one key is present per line */
export type A2UIMessage =
  | { createSurface: CreateSurface }
  | { updateComponents: UpdateComponents }
  | { updateDataModel: UpdateDataModel }
  | { deleteSurface: DeleteSurface };

// ─── Component Catalog — supported component types ────────────────────────

export type ComponentType =
  | "Text"
  | "Icon"
  | "Column"
  | "Row"
  | "Card"
  | "Divider"
  | "List"
  | "Button"
  | "TextField";

// ─── Data Binding — literal values or JSON Pointer paths ──────────────────

/** A value that can be either a literal or a path to the data model */
export interface DataPath {
  path: string;
}

export type DataValue<T = string> = T | DataPath;

// ─── Component Props (per type) ───────────────────────────────────────────

export interface TextProps {
  text: DataValue<string>;
  variant?: "h1" | "h2" | "h3" | "body" | "caption";
}

export interface IconProps {
  name: "person" | "settings" | "search" | "check" | "warning" | "error" | "info";
}

export interface ContainerProps {
  children: string[]; // child component IDs
}

export interface CardProps {
  child: string; // single child component ID
}

export interface ButtonProps {
  text: DataValue<string>;
  action: { name: string; context?: Record<string, unknown> };
  variant?: "primary" | "borderless";
}

export interface TextFieldProps {
  label: DataValue<string>;
  value: DataPath;
}

// ─── Component Definition (as received from updateComponents) ─────────────

/** Props union discriminated by component type */
export type ComponentProps =
  | (TextProps & { component: "Text" })
  | (IconProps & { component: "Icon" })
  | (ContainerProps & { component: "Column" | "Row" | "List" })
  | (CardProps & { component: "Card" })
  | ({ component: "Divider" })
  | (ButtonProps & { component: "Button" })
  | (TextFieldProps & { component: "TextField" });

/** A single component entry in the adjacency list */
export interface ComponentDef {
  id: string;
  component: ComponentType;
  // All other keys are component-specific props
  [key: string]: unknown;
}

// ─── Surface State (accumulated on client) ────────────────────────────────

/** A fully parsed surface with component map and data model */
export interface SurfaceState {
  surfaceId: string;
  catalogId: string;
  /** Component ID → ComponentDef */
  components: Map<string, ComponentDef>;
  /** The merged data model object */
  dataModel: Record<string, unknown>;
  /** Root component ID (defaults to "root") */
  rootId: string;
}

// ─── Render Tree (resolved for rendering) ─────────────────────────────────

/** A node in the resolved render tree, ready for Vue rendering */
export interface RenderNode {
  id: string;
  component: ComponentType;
  /** Resolved props with all data bindings evaluated */
  props: Record<string, unknown>;
  /** Resolved child RenderNodes */
  children: RenderNode[];
}

// ─── Parsed Result — what the parser returns from raw text ─────────────────

/** A single line after parsing: could be an A2UI message, a text line, or invalid */
export interface ParsedA2UILine {
  message?: A2UIMessage;
  text?: string;
  error?: string;
}

/** The complete parsed result with surface states built from all messages */
export interface ParsedA2UIResult {
  /** All text lines (non-A2UI content) */
  textLines: string[];
  /** All A2UI messages in order */
  messages: A2UIMessage[];
  /** Built surface states keyed by surfaceId */
  surfaces: Map<string, SurfaceState>;
  /** Parse errors encountered */
  errors: string[];
}
