import client from "./client";
import type { ApiResponse, LoginRequest, RegisterRequest, LoginResponseData, UserInfo } from "@/types";

export async function loginApi(data: LoginRequest): Promise<ApiResponse<LoginResponseData>> {
  const resp = await client.post<ApiResponse<LoginResponseData>>("/auth/login", data);
  return resp.data;
}

export async function registerApi(data: RegisterRequest): Promise<ApiResponse<{ id: number; username: string }>> {
  const resp = await client.post<ApiResponse<{ id: number; username: string }>>("/auth/register", data);
  return resp.data;
}

export async function getMeApi(): Promise<ApiResponse<UserInfo>> {
  const resp = await client.get<ApiResponse<UserInfo>>("/auth/me");
  return resp.data;
}
