package com.project.myapp.Controllers;
import com.github.javafaker.Faker;
import com.project.myapp.DTO.ProductDTO;
import com.project.myapp.DTO.ProductImageDTO;
import com.project.myapp.Model.Product;
import com.project.myapp.Model.ProductImage;
import com.project.myapp.Services.IProductService;
import com.project.myapp.responses.ProductListResponse;
import com.project.myapp.responses.ProductResponse;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.core.io.UrlResource;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.util.StringUtils;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.*;
import java.util.stream.Collectors;

@RestController
@RequestMapping("${api.prefix}/products")
@RequiredArgsConstructor
public class ProductController {
    private final IProductService productService;

    @GetMapping("")
    public ResponseEntity<?> GetProducts(
            @RequestParam(defaultValue = "")String keyword,
            @RequestParam(defaultValue = "0",name = "category_id") Long categoryId,
            @RequestParam(defaultValue = "0") int page
            , @RequestParam(defaultValue = "10") int limit){
        PageRequest pageRequest = PageRequest.of(page, limit,
                Sort.by("createdAt").descending()
                //Sort.by("id").ascending()
        );
            Page<ProductResponse> productPage = productService.getAllProducts(keyword,categoryId,pageRequest);
        int totalPages = productPage.getTotalPages();
        List<ProductResponse> products = productPage.getContent();
        return ResponseEntity.ok(ProductListResponse
                        .builder()
                        .products(products)
                        .totalPages(totalPages)
                        .build()
        );
    }
    @GetMapping("/{id}")
    public ResponseEntity<?> getProductById(@PathVariable("id") Long productId) {
       try {
           Product existingproduct = productService.getProductById(productId);
           return ResponseEntity.ok(ProductResponse.fromProduct(existingproduct));
       }catch (Exception ex){
           return ResponseEntity.badRequest().body(ex.getMessage());
       }
    }
    @GetMapping("/by-ids")
    public ResponseEntity<?> getProductsByIds(@RequestParam("ids") String ids) {
        //eg: 1,3,5,7
        try {
            // Tách chuỗi ids thành một mảng các số nguyên
            List<Long> productIds = Arrays.stream(ids.split(","))
                    .map(Long::parseLong)
                    .collect(Collectors.toList());
            List<Product> products = productService.findProductsByIds(productIds);
            return ResponseEntity.ok(products);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }
    @PostMapping("")
    public ResponseEntity<?> createProduct(
            @Valid @RequestBody ProductDTO productDTO,
            BindingResult result){
        try{
            if(result.hasErrors()){
                HashSet<String> errorMessages = new HashSet<>();
                result.getFieldErrors()
                        .forEach(error -> errorMessages
                                .add(error.getDefaultMessage()));
                return ResponseEntity.badRequest().body(errorMessages);
            }
            Product newProduct = productService.CreateProduct(productDTO);
            return ResponseEntity.ok(newProduct);
        }catch (Exception e){
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }
    @PostMapping(value = "uploads/{id}",consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<?> uploadImages(@PathVariable("id") Long productId,
            @ModelAttribute("files") List<MultipartFile> files) {
        try {
            Product existingProduct = productService.getProductById(productId);
            HashSet<ProductImage> productImages = new HashSet<>();
            files = files == null ? new ArrayList<>() : files;
            if(files.size()>ProductImage.MAXIMUM_IMAGES_PER_PRODUCT){
                return ResponseEntity.badRequest().body("you can only upload maximum "+
                        ProductImage.MAXIMUM_IMAGES_PER_PRODUCT
                        +" images");
            }
            for (MultipartFile file : files) {
                if (file.getSize() == 0) {
                    continue;
                }
                //check size image file
                if (file.getSize() > 10 * 1024 * 1024) { //size>10MB
                    return ResponseEntity.status(HttpStatus.PAYLOAD_TOO_LARGE).
                            body("file is too large! Maximum size is 10MB");
                }
                String contentType = file.getContentType();
                if (contentType == null || !contentType.startsWith("image/")) {
                    return ResponseEntity.status(HttpStatus.UNSUPPORTED_MEDIA_TYPE).
                            body("File must be an image");
                }
                String filename = storeFile(file); //save database table productimage
                ProductImage productImage = productService
                        .createProductImage(existingProduct.getId().longValue(), ProductImageDTO.builder()
                                .imageUrl(filename)
                                .build()
                        );
                productImages.add(productImage);
            }
            return ResponseEntity.ok().body(productImages);
        } catch(Exception e){
            return ResponseEntity.badRequest().body(e.getMessage());
        }


    }
    private String storeFile(MultipartFile file) throws IOException {
        if(!isImageFile(file)||file.getOriginalFilename()==null){
            throw new IOException("Invalid image format");
        }
        String filename = StringUtils.cleanPath(Objects.requireNonNull(file.getOriginalFilename()));
        String uniqueFilename = UUID.randomUUID().toString()+"_"+filename;
        Path uploadDir = Paths.get("uploads");
        if (!Files.exists(uploadDir)){
            Files.createDirectories(uploadDir);
        }
        //fullPath to file
        Path destination = Paths.get(uploadDir.toString(),uniqueFilename);
        //copy
        Files.copy(file.getInputStream(),destination, StandardCopyOption.REPLACE_EXISTING);
        return uniqueFilename;
    }
    private boolean isImageFile(MultipartFile file){
        String contentType = file.getContentType();
        return contentType!=null && contentType.startsWith("image/");
    }
    @PutMapping("/{id}")
    public ResponseEntity<?> UpdateProduct(@PathVariable long id,@RequestBody ProductDTO productDTO ){
        try {
            Product updateProduct = productService.UpdateProduct(id, productDTO);
            return ResponseEntity.ok(updateProduct);
        }catch (Exception ex){
            return ResponseEntity.badRequest().body(ex.getMessage());
        }
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<?> DeleteProduct(@PathVariable long id){
        try{
            if(productService.getProductById(id)==null) {
                return ResponseEntity.badRequest().body("not found id product:"+id);
            }
            productService.deleteProduct(id);
            return ResponseEntity.ok("deleted successfully");

        }catch (Exception ex){
            return ResponseEntity.badRequest().body(ex.getMessage());
        }
    }
    @GetMapping("/images/{imageName}")
    public ResponseEntity<?> viewImage(@PathVariable String imageName){
        try{
            Path imagePath = Paths.get("uploads/"+imageName);
            UrlResource resource = new UrlResource(imagePath.toUri());
            if(resource.exists()){
                return ResponseEntity.ok().contentType(MediaType.IMAGE_JPEG).body(resource);
            }else {
                return ResponseEntity.notFound().build();
            }
        }catch (Exception ex){
            return ResponseEntity.badRequest().body(ex.getMessage());
        }
    }
    /*@PostMapping("/generateFakeProducts")*/
    private ResponseEntity<String> generateFakeProducts()     {
        Faker faker = new Faker();
        int numberProduct=0;
        for(int i=0;i<1000000000;++i){
                String productName = faker.commerce().productName();
                if(productService.isProductExist(productName)){
                    continue;
                }
                numberProduct++;
                ProductDTO productDTO = ProductDTO.builder()
                        .name(productName)
                        .price((float)faker.number().numberBetween(10,90000000))
                        .description(faker.lorem().sentence())
                        .thumbnail("")
                        .categoryId((long)faker.number().numberBetween(2001,2003))
                        .build();
                try {
                    productService.CreateProduct(productDTO);
                }catch (Exception e){
                    return ResponseEntity.badRequest().body(e.getMessage());

                }
        }

        return ResponseEntity.ok("Fake products generated "+numberProduct);
    }
}
