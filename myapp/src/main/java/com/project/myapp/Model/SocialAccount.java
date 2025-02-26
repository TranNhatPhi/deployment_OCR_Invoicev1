package com.project.myapp.Model;

import jakarta.persistence.*;
import lombok.*;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Entity
@Table(name="social_accounts")
public class SocialAccount {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;
    @Column(name = "provider",nullable = false,length = 20)
    private String provider;
    @Column(name="provider_id",length = 50)
    private String providerId;
    @Column(length = 150,nullable = false)
    private String email;
    @Column(length = 100,nullable = false)
    private String name;
}
