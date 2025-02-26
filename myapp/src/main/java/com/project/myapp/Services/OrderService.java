package com.project.myapp.Services;

import com.project.myapp.DTO.CartItemDto;
import com.project.myapp.DTO.OrderDTO;
import com.project.myapp.Model.*;
import com.project.myapp.exceptions.DataNotFoundException;
import com.project.myapp.respositories.OrderDetailRepository;
import com.project.myapp.respositories.OrderRepository;
import com.project.myapp.respositories.ProductRepository;
import com.project.myapp.respositories.UserRepository;
import lombok.RequiredArgsConstructor;
import org.modelmapper.ModelMapper;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

@Service
@RequiredArgsConstructor
public class OrderService implements IOrderService{
    private final UserRepository userRepository;
    private final OrderRepository orderRepository;
    private final ModelMapper modelMapper;
    private final ProductRepository productRepository;
    private final OrderDetailRepository orderDetailRepository;

    @Override
    public Order createOrder(OrderDTO orderDTO) throws DataNotFoundException {
        //check existing userid
        User userExisting =  userRepository.findById(orderDTO.getUserId()).orElseThrow(
                ()->new DataNotFoundException("cannot find user with id: "+orderDTO.getUserId())
        );
        modelMapper.typeMap(OrderDTO.class,Order.class)
                .addMappings(mapper -> mapper.skip(Order::setId));
        Order order = new Order();
        modelMapper.map(orderDTO,order);
        order.setUser(userExisting);
        order.setOrder_date(LocalDate.now());
        order.setStatus(OrderStatus.PENDING);
        //check date >= date today
        LocalDate shippingDate = orderDTO.getShippingDate()==null?LocalDate.now():orderDTO.getShippingDate();
        if(shippingDate.isBefore(LocalDate.now())){
            throw new DataNotFoundException("data must be at least today !");
        }
        order.setShippingDate(shippingDate);
        order.setActive(true);
        order.setTotalMoney(orderDTO.getTotalMoney());
        orderRepository.save(order);
        // Tạo danh sách các đối tượng OrderDetail từ cartItems
        List<OrderDetail> orderDetails = new ArrayList<>();
        for (CartItemDto cartItemDTO : orderDTO.getCartItems()) {
            // Tạo một đối tượng OrderDetail từ CartItemDTO
            OrderDetail orderDetail = new OrderDetail();
            orderDetail.setOrder(order);

            // Lấy thông tin sản phẩm từ cartItemDTO
            Long productId = cartItemDTO.getProductId();
            int quantity = cartItemDTO.getQuantity();

            // Tìm thông tin sản phẩm từ cơ sở dữ liệu (hoặc sử dụng cache nếu cần)
            Product product = productRepository.findById(productId)
                    .orElseThrow(() -> new DataNotFoundException("Product not found with id: " + productId));

            // Đặt thông tin cho OrderDetail
            orderDetail.setProduct(product);
            orderDetail.setNumberOfProducts(quantity);
            // Các trường khác của OrderDetail nếu cần
            orderDetail.setPrice(product.getPrice());

            // Thêm OrderDetail vào danh sách
            orderDetails.add(orderDetail);
        }
        orderDetailRepository.saveAll(orderDetails);
        return order;
    }

    @Override
    public Order getOrderById(long id) {
        return orderRepository.findById(id).orElse(null);
    }

    @Override
    public Order updateOrder(long id, OrderDTO orderDTO) throws DataNotFoundException {
            Order order = orderRepository.findById(id).orElseThrow(()->
                        new DataNotFoundException("Cannot find order with id:"+id));
            User existingUser = userRepository.findById(orderDTO.getUserId()).orElseThrow(()->
                new DataNotFoundException("Cannot find user with id:"+orderDTO.getUserId()));
            modelMapper.typeMap(OrderDTO.class,Order.class)
                    .addMappings(mapper -> mapper.skip(Order::setId));
            modelMapper.map(orderDTO,order);
            order.setUser(existingUser);
        return orderRepository.save(order);
    }

    @Override
    public void deleteOrder(long id) {
        Order order = orderRepository.findById(id).orElse(null);
        //no-hard-delete
        if  (order != null){
            order.setActive(false);
            orderRepository.save(order);
        }
    }



    @Override
    public List<Order> findByUserId(Long userId) {
        return orderRepository.findByUserId(userId);
    }

    @Override
    public Page<Order> getOrdersByKeyword(String keyword, Pageable pageable) {
        return orderRepository.findByKeyword(keyword, pageable);
    }
}
