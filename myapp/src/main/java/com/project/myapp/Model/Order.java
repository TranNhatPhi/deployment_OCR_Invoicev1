package com.project.myapp.Model;

import com.fasterxml.jackson.annotation.JsonBackReference;
import com.fasterxml.jackson.annotation.JsonManagedReference;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.Date;
import java.util.List;

@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Table(name = "orders")
public class Order {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;
    @ManyToOne
    @JoinColumn(name = "user_id")
    private User user;
    @Column(name = "fullname",length = 100)
    private String fullName;
    @Column(name="email",length = 100)
    private String email;
    @Column(name="phone_number",length = 20)
    private String phoneNumber;
    @Column(name="address",nullable = false,length = 200)
    private String address;
    @Column(name="note",length = 100)
    private String note;
    @Column(name="order_date")
    private LocalDate order_date;
    @Column(name="status")
    private String status;
    @Column(name="total_money")
    private Float totalMoney;
    @Column(name = "Shipping_method")
    private String ShippingMethod;
    @Column(name="Shipping_address")
    private String ShippingAddress;
    @Column(name = "Shipping_date")
    private LocalDate ShippingDate;
    @Column(name ="tracking_number")
    private String trackingNumber;
    @Column(name = "payment_method")
    private String paymentMethod;
    @Column(name = "active")
    private Boolean active;

    @OneToMany(mappedBy = "order",cascade = CascadeType.ALL,fetch = FetchType.LAZY)
    @JsonManagedReference
    private List<OrderDetail> orderDetails;

}
