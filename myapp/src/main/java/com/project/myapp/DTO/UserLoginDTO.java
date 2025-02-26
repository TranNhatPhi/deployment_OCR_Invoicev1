package com.project.myapp.DTO;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import lombok.*;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class UserLoginDTO {
    @JsonProperty("phone_number")
    @NotBlank(message = "phone number is required")
    private String phoneNumber;
    @NotBlank(message = "Password cannot be blank")
    private String password;
    @Min(value = 1, message = "You must enter role's Id")
    @JsonProperty("role_id")
    private Integer  roleId;
}
