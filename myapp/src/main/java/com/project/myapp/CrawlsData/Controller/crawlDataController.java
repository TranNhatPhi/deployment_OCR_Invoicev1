package com.project.myapp.CrawlsData.Controller;

import com.github.javafaker.Faker;
import com.project.myapp.DTO.ProductImageDTO;
import com.project.myapp.Model.Category;
import com.project.myapp.Model.Product;
import com.project.myapp.Model.ProductImage;
import com.project.myapp.Services.IProductService;
import com.project.myapp.respositories.CategoryRepository;
import com.project.myapp.respositories.ProductRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.java.Log;
import org.jsoup.Jsoup;
import org.springframework.web.bind.annotation.*;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;

@RestController
@RequestMapping("${api.prefix}/crawldata")
@RequiredArgsConstructor
@Log
public class crawlDataController {
    private final  IProductService productService;
    private final ProductRepository productRepository;
    private final CategoryRepository categoryRepository;

    @PostMapping("/generateFakeProducts1")
    public Object crawlData(@RequestParam String url, @RequestParam Integer categoryId1) throws Exception {
        var doc = Jsoup.connect(url).get();
        var httd = doc.getElementsByClass("listproduct").get(0);
        var listProduct = httd.getElementsByClass("main-contain");
        var listProducts = new ArrayList<Product>();
        Faker faker = new Faker();
        listProduct.forEach(product -> {
            log.info(product.attr("data-name"));
            var urlDescription = product.absUrl("href");
            try {
                var doc1 = Jsoup.connect(urlDescription).get();
                var html1 = doc1.getElementsByClass("content-article");
                    ProductImageDTO productImageDTO = new ProductImageDTO();
                if (!html1.isEmpty()) {
                    Product products = Product.builder()
                            .name(product.attr("data-name"))
                            .price(Float.parseFloat(product.attr("data-price")))
                            .description(doc1.getElementsByTag("meta")
                                    .get(3).attr("content").replaceAll(",",""))
                            .thumbnail(product.getElementsByTag("img").get(0).absUrl("src").isEmpty() ?
                                            product.getElementsByTag("img").get(0).absUrl("data-src") :
                                            product.getElementsByTag("img").get(0).absUrl("src"))
                            .category(Category.builder().id(categoryId1).name(product.attr("data-cate")).build())
                            .build();
                    products.setProductImages(Collections.singleton(
                            ProductImage.builder().product(products).
                                    imageUrl(product.getElementsByTag("img").get(0).absUrl("src").isEmpty() ?
                                            product.getElementsByTag("img").get(0).absUrl("data-src") :
                                            product.getElementsByTag("img").get(0).absUrl("src")).build()));
                    listProducts.add(products);
                }
                log.info(html1.text());
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        });
        return productRepository.saveAll(listProducts);
    }

}
