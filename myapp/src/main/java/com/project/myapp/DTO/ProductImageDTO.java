package com.project.myapp.DTO;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.project.myapp.Model.Product;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ProductImageDTO {
    @Min(value = 1,message = "Price must be greater than or equal to 1")
    @JsonProperty("product_id")
    private Integer productId;
    @Size(min=4,max=200,message = "Image must be between 5 and 200 character")
    @JsonProperty("image_url")
    private String imageUrl;
}
