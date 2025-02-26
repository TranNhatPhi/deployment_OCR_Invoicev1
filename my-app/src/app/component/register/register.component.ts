import { Component, ViewChild } from '@angular/core';
import { HeaderComponent } from '../header/header.component';
import { FooterComponent } from '../footer/footer.component';
import { HomeComponent } from '../home/home.component';
import { BsModalRef, BsModalService } from "ngx-bootstrap/modal";
import { FormsModule, NgForm } from "@angular/forms";
import { NgIf } from "@angular/common";
import { UserService } from "../../services/user.service";
import { HttpClientModule } from "@angular/common/http";
import { RegisterDto } from "../../dtos/user/register.dto";

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [HeaderComponent, FooterComponent, HomeComponent, FormsModule, NgIf, HttpClientModule],
  templateUrl: './register.component.html',
  styleUrl: './register.component.scss'
})
export class RegisterComponent {
  @ViewChild('registerForm') registerForm!: NgForm;
  phone: string;
  password: string;
  confirmPassword: string;
  fullName: string;
  address: string;
  isAccepted: boolean;
  dateOfBirth: Date;
  facebook_account_id: number = 0;
  google_account_id: number = 0;
  role_id: number = 1;
  constructor(private bsModalRef: BsModalRef, private bsModal: BsModalService, private userService: UserService) {
    this.phone = '';
    this.password = '';
    this.confirmPassword = '';
    this.fullName = '';
    this.address = '';
    this.isAccepted = false;
    this.dateOfBirth = new Date();
    this.dateOfBirth.setFullYear(this.dateOfBirth.getFullYear() - 18);
  }
  onPhoneChange() {
    console.log(`phone type : ${this.phone}`)
  }
  onclickRegister() {
    const message = `phone: ${this.phone}` +
      `password: ${this.password}` +
      `confirmPassword: ${this.confirmPassword}` +
      `fullName: ${this.fullName}` +
      `address: ${this.address}` +
      `isAccepted: ${this.isAccepted}` +
      `dateOfBirth: ${this.dateOfBirth}`;
    // alert(message);
    // debugger
    const registerDTO: RegisterDto = {
      "fullname": this.fullName,
      "phone_number": this.phone,
      "address": this.address,
      "password": this.password,
      "retype_password": this.confirmPassword,
      "data_of_birth": this.dateOfBirth,
      "facebook_account_id": 0,
      "google_account_id": 0,
      "role_id": 1
    };
    this.userService.register(registerDTO).subscribe({
      next: (response: any) => {
        //register success return login
        debugger
        this.bsModalRef.hide();
        alert('đăng ký thành công!!!');
      },
      complete: () => {
      },
      error: (error: any) => {
        alert('Cannot register,error:' + error.error);
      }
    });
  }
  checkPasswordMatch() {
    if (this.password !== this.confirmPassword) {
      this.registerForm.form.controls['confirmPassword'].setErrors({ 'passwordMismatch': true });
    }
    else {
      this.registerForm.form.controls['confirmPassword'].setErrors(null);
    }
  }
  calculateAge(dob: Date): number {
    if (!this.dateOfBirth) {
      return 0;  // Return 0 or an appropriate value indicating no valid age calculation possible
    }
    if (!dob) return 0;
    const today = new Date();
    const birthDate = new Date(dob);
    let age = today.getFullYear() - birthDate.getFullYear();
    const m = today.getMonth() - birthDate.getMonth();
    if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
      age--;
    }
    // if(birthDate.getFullYear()+18==today.getFullYear()){
    //   return 0;
    // }
    return age;
  }



  openFormLoginReturn() {
    this.bsModalRef.hide();

  }
}
