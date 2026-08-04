import client from "./client";
import type { ApiResponse } from "@/types";
import type {
  AdminUser,
  AdminUserCreate,
  AdminUserUpdate,
  AdminRole,
  AdminRoleCreate,
  AdminRoleUpdate,
} from "@/types/admin";

// ── Users ──

export async function getUsersApi(): Promise<ApiResponse<AdminUser[]>> {
  const resp = await client.get<ApiResponse<AdminUser[]>>("/admin/users");
  return resp.data;
}

export async function getUserApi(userId: number): Promise<ApiResponse<AdminUser>> {
  const resp = await client.get<ApiResponse<AdminUser>>(`/admin/users/${userId}`);
  return resp.data;
}

export async function createUserApi(data: AdminUserCreate): Promise<ApiResponse<AdminUser>> {
  const resp = await client.post<ApiResponse<AdminUser>>("/admin/users", data);
  return resp.data;
}

export async function updateUserApi(userId: number, data: AdminUserUpdate): Promise<ApiResponse<AdminUser>> {
  const resp = await client.put<ApiResponse<AdminUser>>(`/admin/users/${userId}`, data);
  return resp.data;
}

export async function toggleUserActiveApi(userId: number): Promise<ApiResponse<AdminUser>> {
  const resp = await client.post<ApiResponse<AdminUser>>(`/admin/users/${userId}/toggle-active`);
  return resp.data;
}

// ── Roles ──

export async function getRolesApi(): Promise<ApiResponse<AdminRole[]>> {
  const resp = await client.get<ApiResponse<AdminRole[]>>("/admin/roles");
  return resp.data;
}

export async function getRoleApi(roleId: number): Promise<ApiResponse<AdminRole>> {
  const resp = await client.get<ApiResponse<AdminRole>>(`/admin/roles/${roleId}`);
  return resp.data;
}

export async function createRoleApi(data: AdminRoleCreate): Promise<ApiResponse<AdminRole>> {
  const resp = await client.post<ApiResponse<AdminRole>>("/admin/roles", data);
  return resp.data;
}

export async function updateRoleApi(roleId: number, data: AdminRoleUpdate): Promise<ApiResponse<AdminRole>> {
  const resp = await client.put<ApiResponse<AdminRole>>(`/admin/roles/${roleId}`, data);
  return resp.data;
}

export async function deleteRoleApi(roleId: number): Promise<ApiResponse<null>> {
  const resp = await client.delete<ApiResponse<null>>(`/admin/roles/${roleId}`);
  return resp.data;
}
