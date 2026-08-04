/** Generic API response wrapper. */
export interface ApiResponse<T = unknown> {
  code: number;
  data: T;
  message: string;
}

/** JWT token payload (decoded). */
export interface JwtPayload {
  sub: string;
  exp: number;
}

/** Login request */
export interface LoginRequest {
  username: string;
  password: string;
}

/** Register request */
export interface RegisterRequest {
  username: string;
  password: string;
}

/** User info returned from auth API */
export interface UserInfo {
  id: number;
  username: string;
  is_admin: boolean;
  is_active: boolean;
  role_id: number | null;
  role_name: string | null;
}

/** Login response data */
export interface LoginResponseData {
  access_token: string;
  token_type: string;
  user: UserInfo;
}
