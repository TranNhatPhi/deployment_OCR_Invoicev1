package com.project.myapp.Services;

import com.project.myapp.DTO.OrderDetailDTO;
import com.project.myapp.Model.OrderDetail;

import java.util.List;

public interface IOrderDetailService {
    OrderDetail createOrderDetail(OrderDetailDTO orderDetailDTO);
    OrderDetail getOrderDetail(Long id);
    OrderDetail updateOrderDetail(Long id,OrderDetailDTO orderDetailDTO);
    void deleteById(Long id);
    List<OrderDetail> findByOrderId(Long orderId);

}
