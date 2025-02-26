//package com.project.myapp.configurations;
//
//import org.springframework.context.annotation.Bean;
//import org.springframework.context.annotation.Configuration;
//import org.springframework.web.cors.CorsConfiguration;
//import org.springframework.web.cors.CorsConfigurationSource;
//import org.springframework.web.cors.UrlBasedCorsConfigurationSource;
//
//@Configuration
//public class CorsConfig {
//    @Bean
//    public CorsConfigurationSource corsConfiguration() {
//        var corsConfig = new CorsConfiguration();
//        corsConfig.applyPermitDefaultValues();
//        corsConfig.setAllowCredentials(true);
//        corsConfig.addAllowedOriginPattern("*");
//        corsConfig.addAllowedHeader("*");
//        corsConfig.addAllowedMethod("*");
//        var source = new UrlBasedCorsConfigurationSource();
//        source.registerCorsConfiguration("/**", corsConfig);
//        return source;
//    }
//
//}
