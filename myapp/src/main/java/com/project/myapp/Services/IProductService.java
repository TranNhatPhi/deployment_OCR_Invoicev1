package com.project.myapp.Services;


import com.project.myapp.DTO.ProductDTO;
import com.project.myapp.DTO.ProductImageDTO;
import com.project.myapp.Model.Product;
import com.project.myapp.Model.ProductImage;
import com.project.myapp.exceptions.DataNotFoundException;
import com.project.myapp.exceptions.InvalidParamException;
import com.project.myapp.responses.ProductResponse;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public interface IProductService {

    Product getProductById(long productId) throws DataNotFoundException, Exception;
    Product CreateProduct(ProductDTO productDTO) throws Exception;
    Page<ProductResponse> getAllProducts(String keyword,Long categoryId, PageRequest pageRequest);
    Product UpdateProduct(long id, ProductDTO productDTO) throws Exception;
    void deleteProduct(long id);
    boolean isProductExist(String productName);
    ProductImage createProductImage(Long productId, ProductImageDTO productImageDTO) throws DataNotFoundException, InvalidParamException;
    List<Product> findProductsByIds(List<Long> productIds);
}
