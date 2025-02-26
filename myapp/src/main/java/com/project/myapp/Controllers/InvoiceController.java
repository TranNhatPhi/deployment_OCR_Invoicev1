package com.project.myapp.Controllers;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatusCode;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.http.client.MultipartBodyBuilder;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

import java.io.File;
import java.util.Map;

@RestController
@RequestMapping("${api.prefix}/invoices")
public class InvoiceController {

    private final WebClient webClient;

    @Autowired
    public InvoiceController(WebClient webClient) {
        this.webClient = webClient;
    }

    // 1. GET all invoices
    @GetMapping
    public Mono<String> getAllInvoices() {
        return webClient.get()
                .uri("/api/get_data")
                .retrieve()
                .bodyToMono(String.class);
    }

    // 2. GET invoice by image_index
    @GetMapping("/{imageIndex}")
    public Mono<String> getInvoiceByIndex(@PathVariable int imageIndex) {
        return webClient.get()
                .uri("/api/get_invoice_info/" + imageIndex)
                .retrieve()
                .bodyToMono(String.class);
    }

    // 3. GET texts from invoices
    @GetMapping("/texts")
    public Mono<String> getTexts() {
        return webClient.get()
                .uri("/api/get_texts")
                .retrieve()
                .bodyToMono(String.class);
    }

    // 4. GET texts by image_index
    @GetMapping("/texts/{imageIndex}")
    public Mono<String> getTextsByIndex(@PathVariable int imageIndex) {
        return webClient.get()
                .uri("/api/get_texts/" + imageIndex)
                .retrieve()
                .bodyToMono(String.class);
    }
    // 6. GET image
    @GetMapping("/get-image")
    public Mono<ResponseEntity<String>> getImage(@RequestParam("filename") String filename) {
        System.out.println("Received request to fetch image");

        // Đảm bảo đây là URL đầy đủ của API Python
        String imageUrl = "/api/uploads/" + filename;

        // Nếu ảnh tồn tại, trả về đường dẫn URL của ảnh
        return webClient
                .get()
                .uri(imageUrl)  // Thêm tên file vào URL
                .header("Accept", "image/jpeg")  // Chỉ định chấp nhận hình ảnh (header thêm vào)
                .retrieve()
                .onStatus(HttpStatusCode::isError, response -> {
                    System.out.println("Error from Flask: " + response.statusCode());
                    return Mono.error(new RuntimeException("Failed to fetch image"));
                })
                .bodyToMono(byte[].class)  // Trả về ảnh dưới dạng byte[]
                .map(imageBytes -> ResponseEntity
                        .ok()
                        .body("/api/uploads/" + filename))  // Trả về đường dẫn ảnh
                .doOnTerminate(() -> System.out.println("Request completed"))
                .doOnError(e -> System.out.println("Error fetching image: " + e.getMessage()));
    }


    // 5. POST upload an image
// 5. POST upload an image
    @PostMapping(value = "/upload-image", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public Mono<String> uploadImage(@RequestParam("image") MultipartFile imageFile) {
        System.out.println("Received request to upload image");

        if (imageFile == null || imageFile.isEmpty()) {
            System.out.println("No file received");
            return Mono.error(new RuntimeException("File not received"));
        }

        System.out.println("Received file: " + imageFile.getOriginalFilename());

        MultipartBodyBuilder builder = new MultipartBodyBuilder();
        builder.part("image", imageFile.getResource());

        return webClient.post()
                .uri("/api/upload_image")
                .contentType(MediaType.MULTIPART_FORM_DATA)
                .bodyValue(builder.build())
                .retrieve()
                .onStatus(HttpStatusCode::isError, response -> {
                    System.out.println("Error from Flask: " + response.statusCode());
                    return null;
                })
                .bodyToMono(String.class);
    }

    // 6. PUT update invoice
    @PutMapping("/{imageIndex}")
    public Mono<String> updateInvoice(@PathVariable int imageIndex, @RequestBody Map<String, Object> payload) {
        return webClient.put()
                .uri("/api/update_invoice/" + imageIndex)
                .bodyValue(payload)
                .retrieve()
                .bodyToMono(String.class);
    }

    // 7. DELETE an invoice
    @DeleteMapping("/{imageIndex}")
    public Mono<String> deleteInvoice(@PathVariable int imageIndex) {
        return webClient.delete()
                .uri("/api/delete_invoice/" + imageIndex)
                .retrieve()
                .bodyToMono(String.class)
                .doOnTerminate(() -> System.out.println("Hóa đơn đã được xóa thành công"))
                .onErrorResume(e -> Mono.just("Xóa hóa đơn thất bại: " + e.getMessage()));
    }
}

