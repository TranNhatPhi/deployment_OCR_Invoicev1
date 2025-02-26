package com.project.myapp.Model;

import jakarta.persistence.*;
import lombok.*;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Date;
import java.util.List;

@Entity
@Table(name = "users")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class User extends dataTimeModel implements UserDetails {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;
    @Column(name = "fullname",length = 100,nullable = false)
    private String fullName;
    @Column(name = "phone_number",length = 10,nullable = false)
    private String phoneNumber;
    @Column(length = 200,nullable = false)
    private String address;
    @Column(name="password",length = 100,nullable = false)
    private String PassWord; //encrypt
    @Column(name="is_active")
    private boolean active;
    @Column(name="date_of_birth")
    private Date dateOfBrith;
    @Column(name="facebook_account_id")
    private Integer facebookAccountId;
    @Column(name = "google_account_id")
    private Integer googleAccountId;
    @Column(name = "avatar")
    private String avatar;
    @ManyToOne
    @JoinColumn(name="role_id")
    private Role role;


    @Override
    public Collection<? extends GrantedAuthority> getAuthorities() {
            List<SimpleGrantedAuthority> authorities = new ArrayList<>();
        authorities.add(new SimpleGrantedAuthority("ROLE_"+getRole().getName().toUpperCase()));
        //authorities.add(new SimpleGrantedAuthority("ROLE_ADMIN"));
        return authorities;
    }

    @Override
    public String getPassword() {
        return PassWord;
    }

    @Override
    public String getUsername() {
        return phoneNumber;
    }

    @Override
    public boolean isAccountNonExpired() {
        return true;
    }

    @Override
    public boolean isAccountNonLocked() {
        return true;
    }

    @Override
    public boolean isCredentialsNonExpired() {
        return true;
    }

    @Override
    public boolean isEnabled() {
        return true;
    }
}
