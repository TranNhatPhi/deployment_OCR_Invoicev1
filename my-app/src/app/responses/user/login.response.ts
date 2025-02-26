export interface LoginResponse {
  message: string;
  token: string;
  user: {
    name: string;
    avatarUrl: string;
    // Các thông tin khác của người dùng nếu có
  };
}
