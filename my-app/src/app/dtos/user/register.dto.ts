import {IsDate, IsEmpty, IsNotEmpty, IsPhoneNumber, IsString} from "class-validator";

export class RegisterDto{
  @IsString()
  fullname: string;
  @IsPhoneNumber()
  phone_number:string;
  @IsString()
  @IsNotEmpty()
  address:string;
  @IsString()
  @IsNotEmpty()
  password:string;
  @IsString()
  @IsNotEmpty()
  retype_password:string;
  @IsDate()
  data_of_birth:Date;
  facebook_account_id:number;
  google_account_id:number;
  role_id:number;
  constructor(data:any) {
      this.fullname = data.fullname;
      this.phone_number = data.phone_number;
      this.address = data.address;
      this.password = data.password;
      this.retype_password = data.retype_password;
      this.data_of_birth = data.data_of_birth;
      this.facebook_account_id =data.facebook_account_id || 0;
      this.google_account_id = data.google_account_id || 0;
      this.role_id =data.role_id||1;
  }
}
