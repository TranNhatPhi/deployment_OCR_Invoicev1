import { Injectable } from '@angular/core';
import {environment} from "../environments/environment";

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private currentUser: any;
  private apiUrlLogin = environment.apiBaseurl + '/users/login';

  constructor() {

  }

  login(credentials: any) {
    // Giả sử bạn có một API để xử lý đăng nhập

    // Sau khi đăng nhập thành công, lưu thông tin người dùng
    this.currentUser = {
      name: 'Nhật Phi',
      avatarUrl: 'URL_to_avatar'
    };
    localStorage.setItem('currentUser', JSON.stringify(this.currentUser));
  }

  getCurrentUser() {
    return JSON.parse(localStorage.getItem('currentUser') || '{}');
  }

  isLoggedIn() {
    return !!localStorage.getItem('currentUser');
  }

  logout() {
    localStorage.removeItem('currentUser');
  }
}
