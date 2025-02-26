package com.project.myapp.Model;

import com.fasterxml.jackson.annotation.JsonBackReference;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.persistence.*;
import lombok.*;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@Entity
@Builder
@Table(name="product_image")
public class ProductImage {
    public static final int MAXIMUM_IMAGES_PER_PRODUCT =6;
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @ManyToOne
    @JsonBackReference
    @JoinColumn(name = "product_id")
    @JsonIgnore
    private Product product;
    @Column(name="image_url",length = 300)
    @JsonProperty("image_url")
    private String imageUrl;

}
