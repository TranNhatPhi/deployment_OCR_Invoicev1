import {Component, inject, OnInit} from '@angular/core';
import {Router, RouterLink} from "@angular/router";
import {CouponService} from "../../services/coupon.service";
import {CartService} from "../../services/cart.service";
import {ProductService} from "../../services/product.service";
import {TokenService} from "../../services/token.service";
import {FormGroup, FormsModule, ReactiveFormsModule} from "@angular/forms";
import {Product} from "../../models/product";
import {OrderDTO} from "../../dtos/order/order.dto";
import {HeaderComponent} from "../header/header.component";
import {FooterComponent} from "../footer/footer.component";
import {HomeComponent} from "../home/home.component";
import {DecimalPipe, NgForOf, NgIf} from "@angular/common";
import {OrderService} from "../../services/order.service";
import {ApiResponse} from "../../responses/api.response";

@Component({
  selector: 'app-thank-you',
  standalone: true,
  imports: [
    RouterLink,HeaderComponent, FooterComponent, HomeComponent, FormsModule, DecimalPipe, NgForOf, NgIf, ReactiveFormsModule
  ],
  templateUrl: './thank-you.component.html',
  styleUrl: './thank-you.component.scss'
})
export class ThankYouComponent implements OnInit{
  orderData: OrderDTO | null = null;
  constructor(private orderService:OrderService,private cartService:CartService) {}
  ngOnInit(): void {
    debugger;
    const storedOrderData = localStorage.getItem("VNPAYORDER");
    if (storedOrderData) {
      this.orderData = JSON.parse(storedOrderData);
      // Clear the stored order data if you don't need it anymore
      this.orderService.saveUser(this.orderData).subscribe({
        next: (response: any) => {
        alert('Đặt hàng thành công');
          this.cartService.clearCart();
          localStorage.removeItem("VNPAYORDER");
          },
        complete: () => {
      },
        error: (error: any) => {
        alert(`Lỗi khi đặt hàng: ${error}`);
      },
    });
  }
    }
}
