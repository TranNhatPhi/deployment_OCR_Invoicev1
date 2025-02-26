package com.project.myapp.DTO;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.*;

import java.util.Date;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class UserDTO {
    @JsonProperty("fullname")
    private String fullName;
    @JsonProperty("phone_number")
    @NotBlank(message = "phone number is required")
    private String phoneNumber;
    private String address;
    @NotBlank(message = "Password cannot be blank")
    private String password;
    @JsonProperty("retype_password")
    private String retypePassword;

    @JsonProperty("data_of_birth")
    private Date dateOfBirth;

    @JsonProperty("active")
    private boolean active;

    @JsonProperty("facebook_account_id")
    private Integer facebookAccountId;

    @JsonProperty("google_account_id")
    private Integer googleAccountId;
    @JsonProperty("avatar")
    private String avatar;
    @NotNull(message = "Role ID is required")
    @JsonProperty("role_id")
    private Integer roleId;
}
