package com.project.myapp.responses;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.project.myapp.Model.Product;
import com.project.myapp.Model.ProductImage;
import lombok.*;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ProductResponse extends DataTimeResponse {
    private Integer id;
    private String name;
    private float price;
    private String thumbnail;
    private String description;
    @JsonProperty("product_images")
    private Set<ProductImage> productImages = new HashSet<>();

    @JsonProperty("category_id")
    private Long categoryId;
    public static ProductResponse fromProduct(Product product) {
            ProductResponse productResponse = ProductResponse.builder()
                    .id(product.getId())
                    .name(product.getName())
                    .price(product.getPrice())
                    .thumbnail(product.getThumbnail())
                    .description(product.getDescription())
                    .categoryId(product.getCategory().getId().longValue())
                    .productImages(product.getProductImages())
                    .build();
            productResponse.setCreatedAt(product.getCreatedAt());
            productResponse.setUpdatedAt(product.getUpdatedAt());
            return productResponse;
    }
}
