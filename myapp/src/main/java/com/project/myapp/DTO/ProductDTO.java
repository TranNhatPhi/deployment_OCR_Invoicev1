package com.project.myapp.DTO;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.*;
import lombok.*;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ProductDTO {
    @NotBlank(message="Title is requỉred")
    @Size(min=4,max=200,message = "Title must be between 5 and 200 character")
    private String name;
    @Min(value = 0,message = "Price must be greater than or equal to 0")
    @Max(value=1000000000,message ="Price must be less than or equal to 1.000.000.000" )
    @Digits(integer = 10, fraction = 5,message = "phone number must be the digits")
    private float price;
    private String thumbnail;
    private String description;
    @JsonProperty("category_id")
    private Long categoryId;
    private ProductImageDTO productImageDTO;
}
