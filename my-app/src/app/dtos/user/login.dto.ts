import { IsNotEmpty, IsPhoneNumber, IsString } from "class-validator";

export class LoginDTO {
    @IsPhoneNumber()
    phone_number: string;
    @IsNotEmpty()
    @IsString()
    password: string;
    constructor(data: any) {
        this.phone_number = data.phone_number;
        this.password = data.password;
    }
}
