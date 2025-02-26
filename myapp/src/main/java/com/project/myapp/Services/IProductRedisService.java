package com.project.myapp.Services;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.project.myapp.responses.ProductResponse;
import org.springframework.data.domain.PageRequest;

import java.util.List;

public interface IProductRedisService {
    void clear();
    List<ProductResponse> getAllProducts(String keyword, Long categoryId, PageRequest pageRequest) throws JsonProcessingException;
    void saveAllProducts(List<ProductResponse> productResponses,String keyword,Long categoryId,PageRequest pageRequest) throws JsonProcessingException;
}
