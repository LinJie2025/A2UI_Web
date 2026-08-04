/** User displayed in admin pages */
export interface AdminUser {
  id: number;
  username: string;
  is_active: boolean;
  is_admin: boolean;
  role_id: number | null;
  role_name: string | null;
  created_at: string;
  updated_at: string;
}

export interface AdminUserCreate {
  username: string;
  password: string;
  is_active: boolean;
  is_admin: boolean;
  role_id: number | null;
  odoo_api_key: string | null;
}

export interface AdminUserUpdate {
  username?: string;
  password?: string;
  is_active?: boolean;
  is_admin?: boolean;
  role_id?: number | null;
  odoo_api_key?: string | null;
}

export interface AdminRole {
  id: number;
  name: string;
  description: string | null;
  created_at: string;
  tool_names: string[];
}

export interface AdminRoleCreate {
  name: string;
  description: string | null;
  tool_names: string[];
}

export interface AdminRoleUpdate {
  name?: string;
  description?: string | null;
  tool_names?: string[];
}
