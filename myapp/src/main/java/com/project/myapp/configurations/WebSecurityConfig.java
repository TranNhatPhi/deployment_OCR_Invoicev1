package com.project.myapp.configurations;

import com.project.myapp.Model.Role;
import com.project.myapp.filters.JwtTokenFilter;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.CorsConfigurationSource;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;
import org.springframework.web.servlet.config.annotation.EnableWebMvc;


import java.util.List;

import static org.springframework.http.HttpMethod.*;
@Configuration
@EnableWebSecurity
@RequiredArgsConstructor
@EnableWebMvc
@EnableMethodSecurity
public class WebSecurityConfig {
    private final JwtTokenFilter jwtTokenFilter;
    @Value("${api.prefix}")
    private String apiPrefix;
    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
                .csrf(AbstractHttpConfigurer::disable)
                .addFilterBefore(jwtTokenFilter, UsernamePasswordAuthenticationFilter.class)
                .cors(c -> c.configurationSource(corsConfiguration()))
                .authorizeHttpRequests(request ->{  
                    request.requestMatchers(String.format("%s/users/register",apiPrefix),
                            String.format("%s/users/login",apiPrefix)
                    )
                            .permitAll()
                            .requestMatchers(GET,String.format("%s/roles**",apiPrefix)).permitAll()
                            .requestMatchers(GET,String.format("%s/categories**",apiPrefix)).permitAll()

                            .requestMatchers(POST,String.format("%s/categories/**",apiPrefix))
                            .hasAnyRole(Role.ADMIN)
                            .requestMatchers(PUT,String.format("%s/categories/**",apiPrefix))
                            .hasRole(Role.ADMIN)
                            .requestMatchers(DELETE,String.format("%s/categories/**",apiPrefix))
                            .hasRole(Role.ADMIN)

                            .requestMatchers(GET,String.format("%s/products**",apiPrefix))
                            .permitAll()
                            .requestMatchers(GET,String.format("%s/products/**",apiPrefix))
                            .permitAll()
                            .requestMatchers(GET,String.format("%s/products/images/*", apiPrefix))
                            .permitAll()
                            .requestMatchers(POST,String.format("%s/products/**",apiPrefix))
                            .hasAnyRole(Role.ADMIN)
                            .requestMatchers(PUT,String.format("%s/products/**",apiPrefix))
                            .hasRole(Role.ADMIN)
                            .requestMatchers(DELETE,String.format("%s/products/**",apiPrefix))
                            .hasRole(Role.ADMIN)

                            .requestMatchers(GET,String.format("%s/orders/**",apiPrefix))
                            .permitAll()
                            .requestMatchers(POST,String.format("%s/orders/**",apiPrefix))
                            .hasAnyRole(Role.USER)
                            .requestMatchers(PUT,String.format("%s/orders/**",apiPrefix))
                            .hasRole(Role.ADMIN)
                            .requestMatchers(DELETE,String.format("%s/orders/**",apiPrefix))
                            .hasRole(Role.ADMIN)
                            .requestMatchers(GET,String.format("%s/orders/get-orders-by-keyword**",apiPrefix))
                            .hasRole(Role.ADMIN)

                            .requestMatchers(GET,String.format("%s/order-detail/**",apiPrefix))
                            .permitAll()
                            .requestMatchers(POST,String.format("%s/order-detail/**",apiPrefix))
                            .hasAnyRole(Role.USER)
                            .requestMatchers(PUT,String.format("%s/order-detail/**",apiPrefix))
                            .hasRole(Role.ADMIN)
                            .requestMatchers(DELETE,String.format("%s/order-detail/**",apiPrefix))
                            .hasRole(Role.ADMIN)
                            .requestMatchers(POST,String.format("%s/payment/vnpay**",apiPrefix))
                            .hasRole(Role.USER)

                            .requestMatchers(GET,String.format("%s/invoices**",apiPrefix))
                            .permitAll()

                            .requestMatchers(POST,String.format("%s/invoices/upload-image**",apiPrefix))
                            .permitAll()
                            .requestMatchers(DELETE,String.format("%s/invoices/**",apiPrefix))
                            .hasRole(Role.ADMIN)

                            .requestMatchers(POST,String.format("%s/crawldata/generateFakeProducts1/**",apiPrefix))
                            .hasAnyRole(Role.ADMIN)
                            .anyRequest().authenticated();
                });
        return http.build();
        }

    @Bean
    public CorsConfigurationSource corsConfiguration() {
        var corsConfig = new CorsConfiguration();
        corsConfig.applyPermitDefaultValues();
//        corsConfig.setAllowCredentials(true);
//        corsConfig.addAllowedOrigin("*");
//        corsConfig.addAllowedOriginPattern("*");
        corsConfig.setAllowedOrigins(List.of("*"));
//        corsConfig.addAllowedOriginPattern("http://localhost:*");  // Chấp nhận tất cả các cổng trên localhost
        corsConfig.setAllowedMethods(List.of("*"));
        corsConfig.setAllowedHeaders(List.of("*"));
//        corsConfig.addAllowedHeader("*");
//        corsConfig.addAllowedMethod("*");
        var source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", corsConfig);
        return source;
    }
}
