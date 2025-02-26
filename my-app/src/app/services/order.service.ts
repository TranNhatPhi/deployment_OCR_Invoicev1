import {Injectable} from "@angular/core";
import {environment} from "../environments/environment";
import {HttpClient, HttpParams} from "@angular/common/http";
import {Observable} from "rxjs";
import {OrderDTO} from "../dtos/order/order.dto";
import {OrderResponse} from "../responses/order/order.response";
import {ApiResponse} from "../responses/api.response";

@Injectable({

  providedIn: 'root',
})
  export class OrderService {
  private apiUrl = `${environment.apiBaseurl}/orders`;
  private apiGetAllOrders = `${environment.apiBaseurl}/orders/get-orders-by-keyword`;

  constructor(private http: HttpClient) {}

  placeOrder(orderData: OrderDTO): Observable<any> {
    // Gửi yêu cầu đặt hàng
    return this.http.post(this.apiUrl, orderData);
  }
  updateOrder(orderId: number, orderData: OrderDTO): Observable<any> {
    const url = `${environment.apiBaseurl}/orders/${orderId}`;
    return this.http.put<any>(url, orderData);
  }
  saveUser(orderData: OrderDTO | null): Observable<any> {
    // Gửi yêu cầu đặt hàng
    return this.http.post(this.apiUrl, orderData);
  }

  getOrderById(orderId:number): Observable<any> {
    const url = `${environment.apiBaseurl}/orders/${orderId}`;
    return this.http.get(url);
  }
  getAllOrders(keyword:string,
               page: number, limit: number
  ): Observable<ApiResponse> {
    const params = new HttpParams()
      .set('keyword', keyword)
      .set('page', page.toString())
      .set('limit', limit.toString());
    return this.http.get<ApiResponse>(this.apiGetAllOrders, { params });
  }
  deleteOrder(orderId: number): Observable<any> {
    const url = `${environment.apiBaseurl}/orders/${orderId}`;
    return this.http.delete<any>(url);
  }

}
