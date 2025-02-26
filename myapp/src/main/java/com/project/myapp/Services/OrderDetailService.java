package com.project.myapp.Services;

import com.project.myapp.DTO.OrderDetailDTO;
import com.project.myapp.Model.Order;
import com.project.myapp.Model.OrderDetail;
import com.project.myapp.Model.Product;
import com.project.myapp.exceptions.DataNotFoundException;
import com.project.myapp.respositories.OrderDetailRepository;
import com.project.myapp.respositories.OrderRepository;
import com.project.myapp.respositories.ProductRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;
@RequiredArgsConstructor
@Service

public class OrderDetailService implements IOrderDetailService{
    private final OrderRepository orderRepository;
    private final OrderDetailRepository orderDetailRepository;
    private final ProductRepository productRepository;

    @Override
    public OrderDetail createOrderDetail(OrderDetailDTO orderDetailDTO) {
        Order order = orderRepository.findById(orderDetailDTO.getOrderId().longValue())
                .orElseThrow(()->new DataNotFoundException("Cannot find order with id:"+orderDetailDTO.getOrderId()));
        Product product = productRepository.findById(orderDetailDTO.getProductId().longValue())
                .orElseThrow(()->new DataNotFoundException("cannot find product id : "+orderDetailDTO.getProductId()));

        OrderDetail orderDetail = OrderDetail.builder()
                .order(order)
                .product(product)
                .numberOfProducts(orderDetailDTO.getNumberOfProduct())
                .price(orderDetailDTO.getPrice())
                .totalMoney(orderDetailDTO.getTotalMoney())
                .color(orderDetailDTO.getColor())
                .build();
        return orderDetailRepository.save(orderDetail);
    }



    @Override
    public OrderDetail getOrderDetail(Long id) {
        return orderDetailRepository.findById(id).
                orElseThrow(()-> new DataNotFoundException("Cannot find OrderDetail with id:"+id));
    }

    @Override
    public OrderDetail updateOrderDetail(Long id, OrderDetailDTO orderDetailDTO) {
        //check orderDetail existing
        OrderDetail existingOrderDetail = orderDetailRepository.findById(id).orElseThrow(
                ()-> new DataNotFoundException("Cannot find OrderDetail with id:"+id)
        );
        //check order existing
        Order existingOrder = orderRepository.findById(orderDetailDTO.getOrderId().longValue()).orElseThrow(
                ()-> new DataNotFoundException("Cannot find Order with id:"+id)
        );
        Product existingProduct = productRepository.findById(orderDetailDTO.getProductId().longValue()).orElseThrow(
                ()-> new DataNotFoundException("Cannot find Product with id:"+id)
        );
        existingOrderDetail.setPrice(orderDetailDTO.getPrice());
        existingOrderDetail.setNumberOfProducts(orderDetailDTO.getNumberOfProduct());
        existingOrderDetail.setColor(orderDetailDTO.getColor());
        existingOrderDetail.setTotalMoney(orderDetailDTO.getTotalMoney());
        existingOrderDetail.setOrder(existingOrder);
        existingOrderDetail.setProduct(existingProduct);

        return orderDetailRepository.save(existingOrderDetail);
    }

    @Override
    public void deleteById(Long id) {
        orderDetailRepository.deleteById(id);

    }

    @Override
    public List<OrderDetail> findByOrderId(Long orderId) {
        return orderDetailRepository.findByOrderId(orderId);
    }
}
