package com.project.myapp.Controllers;

import com.project.myapp.DTO.OrderDetailDTO;
import com.project.myapp.Model.OrderDetail;
import com.project.myapp.Services.OrderDetailService;
import com.project.myapp.responses.OrderDetailResponse;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.*;

import java.util.HashSet;
import java.util.List;

@RestController
@RequiredArgsConstructor
@RequestMapping("${api.prefix}/order-detail")
public class OrderDetailController {

    private final OrderDetailService orderDetailService;
    @PostMapping
    public ResponseEntity<?> createOrderDetail(@Valid @RequestBody OrderDetailDTO orderDetailDTO,
                                               BindingResult result){
        try{
            if (result.hasErrors()) {
                HashSet<String> errorMessages = new HashSet<>();
                result.getFieldErrors()
                        .forEach(error -> errorMessages.add(error.getDefaultMessage()));
                return ResponseEntity.badRequest().body(errorMessages);
            }
            OrderDetail newOrderDetail = orderDetailService.createOrderDetail(orderDetailDTO);
            return ResponseEntity.ok(OrderDetailResponse.fromOrderDetail(newOrderDetail));

        }catch (Exception ex){
            return ResponseEntity.badRequest().body(ex.getMessage());
        }
    }
    @GetMapping("/{id}")
    public ResponseEntity<?> getOrderDetail(@Valid @PathVariable("id") Long id){
        try {
             OrderDetail orderDetail = orderDetailService.getOrderDetail(id);
            return ResponseEntity.ok(OrderDetailResponse.fromOrderDetail(orderDetail));
        }catch (Exception ex){
            return ResponseEntity.badRequest().body(ex.getMessage());
        }
    }
    @GetMapping("/order/{orderId}")
    public ResponseEntity<?> getOrderDetails(@Valid @PathVariable("orderId") Long orderId){
                try{
                    List<OrderDetail> orderDetails = orderDetailService.findByOrderId(orderId);
                    List<OrderDetailResponse> orderDetailResponses = orderDetails.
                            stream().map(OrderDetailResponse::fromOrderDetail)
                            .toList();
                    return ResponseEntity.ok(orderDetailResponses);
                }catch (Exception ex){
                    return ResponseEntity.badRequest().body(ex.getMessage());
                }
    }
    @PutMapping("/{id}")
    public ResponseEntity<?> updateDataOrderDetail(@Valid @PathVariable("id") Long id,
                                                        @RequestBody OrderDetailDTO orderDetailDTO){
        try{
            OrderDetail orderDetail = orderDetailService.updateOrderDetail(id,orderDetailDTO);
            return ResponseEntity.ok(orderDetail);
        }catch (Exception ex){
            return ResponseEntity.badRequest().body(ex.getMessage());
        }
    }
    @DeleteMapping("/{id}")
    public ResponseEntity<String> deleteOrderDetail(@Valid @PathVariable("id") Long id){
        try{
            orderDetailService.deleteById(id);
            return ResponseEntity.ok("Deleted order detail with id: " + id + " successfully" );
        }catch (Exception ex){
            return ResponseEntity.badRequest().body(ex.getMessage());
        }
    }
}
