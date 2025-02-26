package com.project.myapp.respositories;

import com.project.myapp.Model.Token;
import com.project.myapp.Model.User;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface TokenRepository extends JpaRepository<Token, Long> {
    List<Token> findByUser(User user);
    Token findByToken(String token);
    /*Token findByRefreshToken(String token);*/
}
