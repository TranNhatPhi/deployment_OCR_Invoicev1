package com.project.myapp.Services;

import com.project.myapp.DTO.ProductDTO;
import com.project.myapp.DTO.ProductImageDTO;
import com.project.myapp.Model.Category;
import com.project.myapp.Model.Product;
import com.project.myapp.Model.ProductImage;
import com.project.myapp.exceptions.DataNotFoundException;
import com.project.myapp.exceptions.InvalidParamException;
import com.project.myapp.responses.ProductResponse;
import com.project.myapp.respositories.CategoryRepository;
import com.project.myapp.respositories.ProductImageRepository;
import com.project.myapp.respositories.ProductRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
public class ProductService implements IProductService {
    private final ProductRepository productRepository;
    private final CategoryRepository categoryRepository;
    private final ProductImageRepository productImageRepository;

    @Override
    public Product getProductById(long productId) throws Exception{
        Optional<Product> optionalProduct = productRepository.getDetailProduct(productId);
        if(optionalProduct.isPresent()) {
            return optionalProduct.get();
        }
        throw new DataNotFoundException("Cannot find product with id =" + productId);
    }

    @Override
    public Product CreateProduct(ProductDTO productDTO){
       Category existingCategory = categoryRepository.
                findById(productDTO.getCategoryId()).
                orElseThrow(()-> new DataNotFoundException("cannot find category with id: "+productDTO.getCategoryId()));

       Product product = Product.builder()
                .name(productDTO.getName())
                .description(productDTO.getDescription())
                .price(productDTO.getPrice())
                .thumbnail(productDTO.getThumbnail())
                .description(productDTO.getDescription())
                .category(existingCategory)
                .build();
        return productRepository.save(product);
    }

    @Override
    public Page<ProductResponse> getAllProducts(String keyword,Long categoryId,PageRequest pageRequest) {
        //get list product page and limit
         Page<Product> productPage;
         productPage = productRepository.searchProducts(categoryId,keyword, pageRequest);
        return productPage.map(ProductResponse::fromProduct);
    }

    @Override
    public Product UpdateProduct(long id, ProductDTO productDTO) throws Exception {
        Product existingProduct = getProductById(id);
        if(existingProduct!=null){
            Category existingCategory = categoryRepository.
                    findById(productDTO.getCategoryId()).
                    orElseThrow(()-> new DataNotFoundException("cannot find category with id: "+productDTO.getCategoryId()));
            existingProduct.setName(productDTO.getName());
            existingProduct.setCategory(existingCategory);
            existingProduct.setPrice(productDTO.getPrice());
            existingProduct.setThumbnail(productDTO.getThumbnail());
            existingProduct.setDescription(productDTO.getDescription());
            return productRepository.save(existingProduct);
        }
        return null;
    }

    @Override
    public void deleteProduct(long id) {
        Optional<Product> productOptional = productRepository.findById(id);
        productOptional.ifPresent(productRepository::delete);
    }

    @Override
    public boolean isProductExist(String productName) {
        return  productRepository.existsByName(productName);
    }
    @Override
    public ProductImage createProductImage(Long productId, ProductImageDTO productImageDTO) throws DataNotFoundException, InvalidParamException {
        Product existingProduct = productRepository.
                findById(productId).
                orElseThrow(()-> new DataNotFoundException("cannot find product with id: "+productImageDTO.getProductId()));
        ProductImage productImage = ProductImage.builder()
                .product(existingProduct)
                .imageUrl(productImageDTO.getImageUrl())
                .build();
        int size = productImageRepository.findByProductId(productId).size();
        if(size>=ProductImage.MAXIMUM_IMAGES_PER_PRODUCT){
            throw new InvalidParamException("number of images must be <="+ProductImage.MAXIMUM_IMAGES_PER_PRODUCT);
        }
        return productImageRepository.save(productImage);
    }

    @Override
    public List<Product> findProductsByIds(List<Long> productIds) {
        return productRepository.findProductsByIds(productIds);
    }
}
