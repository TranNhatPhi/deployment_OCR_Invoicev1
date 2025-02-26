package com.project.myapp.responses;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.*;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class loginResponse {
    @JsonProperty("message")
    private String message;
    @JsonProperty("token")
    private String token;
}
