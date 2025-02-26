import {Component, inject, OnInit} from '@angular/core';
import {HeaderComponent} from '../header/header.component';
import {FooterComponent} from '../footer/footer.component';
import {HomeComponent} from '../home/home.component';
import {CartService} from "../../services/cart.service";
import {ProductService} from "../../services/product.service";
import {OrderService} from "../../services/order.service";
import {Product} from "../../models/product";
import {OrderDTO} from "../../dtos/order/order.dto";
import {FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators} from "@angular/forms";
import {DecimalPipe, NgForOf, NgIf} from "@angular/common";
import {TokenService} from "../../services/token.service";
import {Router} from "@angular/router";
import {CouponService} from "../../services/coupon.service";
import {ApiResponse} from "../../responses/api.response";
import {PaymentService} from "../../services/payment.service";

@Component({
  selector: 'app-order',
  standalone: true,
  imports: [HeaderComponent, FooterComponent, HomeComponent, FormsModule, DecimalPipe, NgForOf, NgIf, ReactiveFormsModule],
  templateUrl: './order.component.html',
  styleUrl: './order.component.scss'
})
export class OrderComponent implements OnInit {

  private couponService = inject(CouponService);
  private cartService = inject(CartService);
  private productService = inject(ProductService);
  private tokenService = inject(TokenService);
  private router = inject(Router);

  orderForm: FormGroup; // Đối tượng FormGroup để quản lý dữ liệu của form
  cartItems: { product: Product, quantity: number }[] = [];
  totalAmount: number = 0; // Tổng tiền
  couponDiscount: number = 0; //số tiền được discount từ coupon
  couponApplied: boolean = false;
  cart: Map<number, number> = new Map();
  orderData: OrderDTO = {
    status: 'pending',
    user_id: 0, // Thay bằng user_id thích hợp
    fullname: '', // Khởi tạo rỗng, sẽ được điền từ form
    email: '', // Khởi tạo rỗng, sẽ được điền từ form
    phone_number: '', // Khởi tạo rỗng, sẽ được điền từ form
    address: '', // Khởi tạo rỗng, sẽ được điền từ form
    note: '', // Có thể thêm trường ghi chú nếu cần
    total_money: 0, // Sẽ được tính toán dựa trên giỏ hàng và mã giảm giá
    payment_method: 'cod', // Mặc định là thanh toán khi nhận hàng (COD)
    shipping_method: 'express', // Mặc định là vận chuyển nhanh (Express)
    coupon_code: '', // Sẽ được điền từ form khi áp dụng mã giảm giá
    cart_items: []
  };

  constructor(
    private formBuilder: FormBuilder,
    private orderService: OrderService,
    private paymentService: PaymentService
  ) {// Tạo FormGroup và các FormControl tương ứng
    this.orderForm = this.formBuilder.group({
      fullname: ['', Validators.required], // fullname là FormControl bắt buộc
      email: ['', [Validators.email]], // Sử dụng Validators.email cho kiểm tra định dạng email
      phone_number: ['', [Validators.required, Validators.minLength(6)]], // phone_number bắt buộc và ít nhất 6 ký tự
      address: ['', [Validators.required, Validators.minLength(5)]], // address bắt buộc và ít nhất 5 ký tự
      note: [''],
      couponCode: [''],
      shippingmethod: ['express'],
      payment_method: ['cod']
    });
  }

  ngOnInit(): void {
    debugger
    //this.cartService.clearCart();
    this.orderData.user_id = this.tokenService.getUserId();
    // Lấy danh sách sản phẩm từ giỏ hàng
    debugger
    const cart = this.cartService.getCart();
    const productIds = Array.from(cart.keys()); // Chuyển danh sách ID từ Map giỏ hàng

    // Gọi service để lấy thông tin sản phẩm dựa trên danh sách ID
    // Gọi service để lấy thông tin sản phẩm dựa trên danh sách ID
    debugger
    if (productIds.length === 0) {
      return;
    }
    this.productService.getProductsByIds(productIds).subscribe({
      next: (products) => {
        debugger
        // Lấy thông tin sản phẩm và số lượng từ danh sách sản phẩm và giỏ hàng
        this.cartItems = productIds.map((productId) => {
          debugger
          const product = products.find((p) => p.id === productId);
          return {
            product: product!,
            quantity: cart.get(productId)!
          };
        });
        console.log('haha');
      },
      complete: () => {
        debugger;
        this.calculateTotal();
      },
      error: (error: any) => {
        debugger;
        console.error('Error fetching detail:', error);
      }
    });
  }

  placeOrder() {
    console.log(this.orderForm)
    debugger;
    if (this.orderForm.valid) {
      this.orderData = {
        ...this.orderData,
        ...this.orderForm.value
      };
      this.orderData.cart_items = this.cartItems.map(cartItem => ({
        product_id: cartItem.product.id,
        quantity: cartItem.quantity
      }));

      this.orderData.total_money = this.totalAmount;
      // Dữ liệu hợp lệ, bạn có thể gửi đơn hàng đi
      if (this.orderForm.get('payment_method')?.value === 'VNPAY') {
        /* window.location.href = response.data; // Redirect to VNPAY payment URL*/
        this.paymentService.initiatePayment({
          amount: this.orderData.total_money
        }).subscribe({
          next: (response: any) => {
            localStorage.setItem("VNPAYORDER",JSON.stringify(this.orderData));
            window.location.href = response.url; // Redirect to VNPAY payment URL
          },
          error: (error: any) => {
            alert(`Lỗi khi thanh toán: ${error}`);
          }
        });
      } else {
        this.orderService.placeOrder(this.orderData).subscribe({
          next: (response: ApiResponse) => {
            alert('Đặt hàng thành công');
            this.cartService.clearCart();
            this.router.navigate(['/thanhtoansuccess']).then(() => {
              console.log('oke')
            });

          },
          complete: () => {
            this.calculateTotal();
          },
          error: (error: any) => {
            alert(`Lỗi khi đặt hàng: ${error}`);
          },
        });
      }
    } else {
      // Hiển thị thông báo lỗi hoặc xử lý khác
      alert('Dữ liệu không hợp lệ. Vui lòng kiểm tra lại.');
    }
  }

  // Hàm tính tổng tiền
  decreaseQuantity(index: number): void {
    if (this.cartItems[index].quantity > 1) {
      this.cartItems[index].quantity--;
      // Cập nhật lại this.cart từ this.cartItems
      this.updateCartFromCartItems();
      this.calculateTotal();
    }
  }

  increaseQuantity(index: number): void {
    this.cartItems[index].quantity++;
    // Cập nhật lại this.cart từ this.cartItems
    this.updateCartFromCartItems();
    this.calculateTotal();
  }

  // Hàm tính tổng tiền
  calculateTotal(): void {
    this.totalAmount = this.cartItems.reduce(
      (total, item) => total + item.product.price * item.quantity,
      0
    );
  }
  confirmDelete(index: number): void {
    if (confirm('Bạn có chắc chắn muốn xóa sản phẩm này?')) {
      // Xóa sản phẩm khỏi danh sách cartItems
      this.cartItems.splice(index, 1);
      // Cập nhật lại this.cart từ this.cartItems
      this.updateCartFromCartItems();
      // Tính toán lại tổng tiền
      this.calculateTotal();
    }
  }
  // Hàm xử lý việc áp dụng mã giảm giá
  applyCoupon(): void {
    debugger
    const couponCode = this.orderForm.get('couponCode')!.value;
    if (!this.couponApplied && couponCode) {
      this.calculateTotal();
      this.couponService.calculateCouponValue(couponCode, this.totalAmount)
        .subscribe({
          next: (apiResponse: ApiResponse) => {
            this.totalAmount = apiResponse.data;
            this.couponApplied = true;
          }
        });
    }
  }
  private updateCartFromCartItems(): void {
    this.cart.clear();
    this.cartItems.forEach((item) => {
      this.cart.set(item.product.id, item.quantity);
    });
    this.cartService.setCart(this.cart);
  }
}
