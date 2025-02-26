import {Component, OnInit} from '@angular/core';
import { HeaderComponent } from '../header/header.component';
import { FooterComponent } from '../footer/footer.component';
import { HomeComponent } from '../home/home.component';
import {CurrencyPipe, DecimalPipe, NgForOf, NgIf} from "@angular/common";
import {FormsModule} from "@angular/forms";
import {OrderService} from "../../services/order.service";
import {OrderDetail} from "../../models/order.detail";
import {OrderResponse} from "../../responses/order/order.response";
import {HttpErrorResponse} from "@angular/common/http";
import {ActivatedRoute} from "@angular/router";

@Component({
  selector: 'app-order-confirm',
  standalone: true,
  imports: [HeaderComponent, FooterComponent, HomeComponent, CurrencyPipe, NgForOf, FormsModule, DecimalPipe, NgIf],
  templateUrl: './order-confirm.component.html',
  styleUrl: './order-confirm.component.scss'
})
export class OrderConfirmComponent implements OnInit {
  orderResponse: OrderResponse = {
    id: 0, // Hoặc bất kỳ giá trị số nào bạn muốn
    user_id: 0,
    fullname: '',
    phone_number: '',
    email: '',
    address: '',
    note: '',
    order_date: new Date(),
    status: '',
    total_money: 0, // Hoặc bất kỳ giá trị số nào bạn muốn
    shipping_method: '',
    shipping_address: '',
    shipping_date: new Date(),
    payment_method: '',
    active:true,
    order_details: [] // Một mảng rỗng
  };
  constructor(
    private orderService: OrderService,
    private route: ActivatedRoute
  ) {}

  ngOnInit(): void {
    this.getOrderDetails();
  }

  getOrderDetails(): void {
    debugger
    const orderId = Number(this.route.snapshot.paramMap.get('id'));
      this.orderService.getOrderById(orderId).subscribe({
        next: (apiResponse: any) => {
          debugger;
          const response = apiResponse.data
          this.orderResponse.id = response.id;
          this.orderResponse.user_id = response.user_id;
          this.orderResponse.fullname = response.fullname;
          this.orderResponse.email = response.email;
          this.orderResponse.phone_number = response.phone_number;
          this.orderResponse.address = response.address;
          this.orderResponse.note = response.note;
          this.orderResponse.order_date = new Date(
            response.order_date[0],
            response.order_date[1] - 1,
            response.order_date[2]
          );

          this.orderResponse.order_details = response.order_details
            .map((order_detail: OrderDetail) => {
              return order_detail;
            });
          this.orderResponse.payment_method = response.payment_method;
          this.orderResponse.shipping_date = new Date(
            response.shipping_date[0],
            response.shipping_date[1] - 1,
            response.shipping_date[2]
          );

          this.orderResponse.shipping_method = response.shipping_method;

          this.orderResponse.status = response.status;
          this.orderResponse.total_money = response.total_money;
        },
        complete: () => {
          debugger;
        },
        error: (error: HttpErrorResponse) => {
          debugger;
          console.error(error?.error?.message ?? '');
        }
      });
  }
}

