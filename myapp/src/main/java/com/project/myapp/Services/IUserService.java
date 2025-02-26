package com.project.myapp.Services;

import com.project.myapp.DTO.UpdateUserDTO;
import com.project.myapp.DTO.UserDTO;
import com.project.myapp.Model.User;
import com.project.myapp.exceptions.DataNotFoundException;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

public interface IUserService {
    User CreateUser(UserDTO userDTO)throws Exception;
    String login(String phoneNumber, String password);
    User getUserDetailsFromToken(String token) throws Exception;
    User updateUser(Integer userId, UpdateUserDTO updatedUserDTO) throws Exception;
    Page<User> findAll(String keyword, Pageable pageable) throws Exception;
    void resetPassword(Long userId, String newPassword)
            throws Exception;
    void blockOrEnable(Long userId, Boolean active) throws DataNotFoundException;
}
