import {Inject, inject, Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Observable} from "rxjs";
import {RegisterDto} from "../dtos/user/register.dto";
import {LoginDTO} from '../dtos/user/login.dto';
import {environment} from "../environments/environment";
import {UserResponse} from "../responses/user/user.response";
import {UpdateUserDTO} from "../dtos/user/update.user.dto";
import {HttpUtilService} from "./http.util.service";
import {DOCUMENT} from "@angular/common";

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private apiUrlRegister = environment.apiBaseurl + '/users/register';
  private apiUrlLogin = environment.apiBaseurl + '/users/login';
  private apiUserDetail = environment.apiBaseurl + '/users/details';
  private http = inject(HttpClient);
  private httpUtilService = inject(HttpUtilService);
  localStorage?:Storage;

  constructor(
    @Inject(DOCUMENT) private document: Document
  ) {
    this.localStorage = document.defaultView?.localStorage;
  }
  private apiConfig = {
    headers: this.httpUtilService.createHeaders(),
  }

  private createHeaders(): HttpHeaders {
    return new HttpHeaders({
      'Accept-Language': 'vi'
    });
  }

  register(registerDTO: RegisterDto): Observable<any> {
    return this.http.post(this.apiUrlRegister, registerDTO);
  }

  login(loginDTO: LoginDTO): Observable<any> {
    return this.http.post(this.apiUrlLogin, loginDTO);
  }

  getUserDetail(token: string | null) {
    return this.http.post(this.apiUserDetail, {}, {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      })
    })
  }

  updateUserDetail(token: string | null, updateUserDTO: UpdateUserDTO) {
    debugger
    let userResponse = this.getUserResponseFromLocalStorage();
    return this.http.put(`${this.apiUserDetail}/${userResponse?.id}`,updateUserDTO,{
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      })
    })
  }

  saveUserResponseToLocalStorage(userResponse?: UserResponse) {
    try {
      debugger
      if (userResponse == null || !userResponse) {
        return;
      }
      // Convert the userResponse object to a JSON string
      const userResponseJSON = JSON.stringify(userResponse);
      // Save the JSON string to local storage with a key (e.g., "userResponse")
      localStorage.setItem('user', userResponseJSON);
      console.log('User response saved to local storage.');
    } catch (error) {
      console.error('Error saving user response to local storage:', error);
    }
  }

  getUserResponseFromLocalStorage() {
    try {
      // Retrieve the JSON string from local storage using the key
      const userResponseJSON = localStorage.getItem('user');
      if (userResponseJSON == null) {
        return null;
      }
      // Parse the JSON string back to an object
      const userResponse = JSON.parse(userResponseJSON!);
      console.log('User response retrieved from local storage.');
      return userResponse;
    } catch (error) {
      console.error('Error retrieving user response from local storage:', error);
      return null; // Return null or handle the error as needed
    }
  }

  removeUserFromLocalStorage(): void {
    try {
      // Remove the user data from local storage using the key
      localStorage.removeItem('user');
      console.log('User data removed from local storage.');
    } catch (error) {
      console.error('Error removing user data from local storage:', error);
      // Handle the error as needed
    }
  }
  getUsers(params: { page: number, limit: number, keyword: string }): Observable<any> {
    const url = `${environment.apiBaseurl}/users`;
    return this.http.get<any>(url, { params: params });
  }

  resetPassword(userId: number): Observable<any> {
    const url = `${environment.apiBaseurl}/users/reset-password/${userId}`;
    return this.http.put<any>(url, null, this.apiConfig);
  }

  toggleUserStatus(params: { userId: number, enable: boolean }): Observable<any> {
    const url = `${environment.apiBaseurl}/users/block/${params.userId}/${params.enable ? '1' : '0'}`;
    return this.http.put<any>(url, null, this.apiConfig);
  }
}
