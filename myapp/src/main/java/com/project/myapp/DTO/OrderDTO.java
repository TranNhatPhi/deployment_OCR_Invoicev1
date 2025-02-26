package com.project.myapp.DTO;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDate;
import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class OrderDTO {
    @JsonProperty("user_id")
    @Min(value = 1,message = "User's ID must be >= 1")
    private Long userId;
    @JsonProperty("fullname")
    private String fullName;
    private String email;
    private String status;
    @JsonProperty("phone_number")
    @NotBlank(message = "phone number is required")
    @Size(min =10,max = 10,message = "phone number must be at 10 characters")
    @Digits(integer = 10, fraction = 0,message = "phone number must be the digits")
    private String phoneNumber;
    private String address;
    private String note;
    private boolean active;
    @JsonProperty("total_money")
    @Min(value = 0,message = "total money must be >= 0")
    private Float totalMoney;
    @JsonProperty("shipping_method")
    private String shippingMethod;
    @JsonProperty("shipping_address")
    private String shippingAddress;
    @JsonProperty("shipping_date")
    private LocalDate shippingDate;

    @JsonProperty("payment_method")
    private String paymentMethod;
    @JsonProperty("cart_items")
    private List<CartItemDto> cartItems;

}
