import {error} from "@angular/compiler-cli/src/transformers/util";

declare var google:any;

import {Component, inject, OnInit} from '@angular/core';
import { SharedModule } from "../../shared-module";
import { BsModalService, BsModalRef } from "ngx-bootstrap/modal";
import { RegisterComponent } from "../register/register.component";
import { IsNotEmpty, IsPhoneNumber, IsString } from "class-validator";
import { HttpClientModule } from "@angular/common/http";
import { UserService } from '../../services/user.service';
import { TokenService } from '../../services/token.service';
import { LoginDTO } from '../../dtos/user/login.dto';
import { LoginResponse } from '../../responses/user/login.response';
import {AuthService} from "../../services/auth.service";
import {RoleService} from "../../services/role.service";
import {Role} from "../../models/role";
import {Router} from "@angular/router";
import {UserResponse} from "../../responses/user/user.response";
import {NgToastModule, NgToastService} from "ng-angular-popup";

@Component({
  selector: 'app-login',
  standalone: true,
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss',
  imports: [SharedModule,HttpClientModule,NgToastModule]
})
export class LoginComponent implements OnInit{
  private router = inject(Router);
  @IsPhoneNumber()
  phone: string;
  @IsString()
  @IsNotEmpty()
  password: string;
  roles:Role[] = [];
  rememberMe:boolean = true;
  selectedRole:Role | undefined;
  userResponse?: UserResponse
  constructor( private roleService:RoleService,private toast:NgToastService,
               private bsModal: BsModalService, private userService: UserService, private tokenService: TokenService) {
    this.phone = '';
    this.password = '';
  }
  onPhoneChange() {
    console.log(`phone type : ${this.phone}`)
  }
  ngOnInit(){
    debugger;

    this.roleService.getRoles().subscribe({
        next: (roles:Role[]) => {
        debugger
        this.roles= roles;
        this.selectedRole = roles.length>0?roles[0]:undefined;

      },
      error: (error: any)=>{
        debugger
        console.error('Error getting roles:',error);
    }
    });
    this.loadGoogleAPI();
  }
  private decodeToken(token:string){
    return JSON.parse(atob(token.split(".")[1]));
  }
  handleLogin(response:any){
      if(response) {
        //decode the code
        const payLoad = this.decodeToken(response.credential);
        //store in session
        sessionStorage.setItem("loggedInUser", JSON.stringify(payLoad));
        localStorage.setItem("loggedInUser", JSON.stringify(payLoad));
        //navigate to home/browse
         this.router.navigate(['browse']).then(() => {
           console.log('Navigation ended successfully')
         }).catch((error)=>{
                console.log("failed")
        });
      }
  }
  loadGoogleAPI() {
    const script = document.createElement('script');
    script.src = 'https://accounts.google.com/gsi/client';
    script.async = true;
    script.defer = true;
    script.onload = () => this.initializeGoogleAPI();
    document.head.appendChild(script);
  }

  initializeGoogleAPI() {
    google.accounts.id.initialize({
      client_id: '276940334800-16ni35suaibq3mdcgs3iudp5etg77nus.apps.googleusercontent.com',
      callback: (response: any) => {
        this.handleLogin(response);
        console.log('Google API response:', response);
        // Handle the responses
        console.log(atob(response.credential));
      }
    });

    google.accounts.id.renderButton(
      document.getElementById('google-btn'),
      {
        theme: 'filled_blue',
        size: 'large',
        shape: 'rectangle',
        width:700

      }
    );
  }

  onclickLogin() {
    const message = `phone: ${this.phone}` +
      `password: ${this.password}`;
    //alert(message);
    debugger

    const loginDTO: LoginDTO = {
      phone_number: this.phone,
      password: this.password,
      /*role_id: this.selectedRole?.id ?? 1*/
    };
    this.userService.login(loginDTO).subscribe({
      next: (response: LoginResponse) => {
        const { token } = response;
        if (this.rememberMe) {
          this.tokenService.setToken(token);
          this.userService.getUserDetail(token).subscribe({
            next: (response: any) => {
              this.userResponse = {
                ...response,
                date_of_birth: new Date(response.date_of_birth),
              };
              this.userService.saveUserResponseToLocalStorage(this.userResponse);
              if(this.userResponse?.role.name=='admin'){
                this.router.navigate(['/admin']).then(() => {
                  /*alert('Navigation ended successfully');*/
                  this.toast.success("đăng nhập thành công!!!","Login",5000);
                  location.reload();
                }).catch((error) => {
                  console.log('failed');
                });
              }
              else if(this.userResponse?.role.name=='user') {
                this.router.navigate(['/']).then(() => {

                  alert('Navigation ended successfully');
                  this.toast.success("đăng nhập thành công!!!","Login",5000);
                  location.reload();
                }).catch((error) => {
                  alert('failed');
                });
              }
            },
            complete: () => {
            },
            error: (error: any) => {
              debugger;
              alert(error.error.message);
            }
          })
        }
      },
      complete: () => {
        debugger;
      },
      error: (error: any) => {
        debugger;
        alert("sai tài khoản hoặc mật khẩu vui lòng kiểm tra lại !!!");
      }
    });
  }

  openformregister() {
    this.bsModal.show(RegisterComponent, {
    })
  }
}
