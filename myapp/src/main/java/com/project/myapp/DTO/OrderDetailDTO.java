package com.project.myapp.DTO;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.Digits;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class OrderDetailDTO {
    @JsonProperty("order_id")
    private Integer orderId;
    @JsonProperty("product_id")
    private Integer productId;
    @Min(value = 0,message = "Price must be greater than or equal to 0")
    @Max(value=1000000000,message ="Price must be less than or equal to 1.000.000.000" )
    @Digits(integer = 10, fraction = 5,message = "price must be the digits")
    private Float price;
    @Digits(integer = 10, fraction = 0,message = "numberOfProduct must be the digits")
    @Min(value = 1,message = "numberOfProduct must be greater than or equal to 1")
    @JsonProperty("number_of_product")
    private Integer numberOfProduct;
    @Min(value = 0,message = "Price must be greater than or equal to 0")
    @Digits(integer = 10, fraction = 5,message = "total money must be the digits")
    @JsonProperty("total_money")
    private Float totalMoney;
    private String color;
}
