import {HttpClient, HttpParams} from "@angular/common/http";
import {environment} from "../environments/environment";
import {Observable} from "rxjs";
import {Injectable} from "@angular/core";
import {ApiResponse} from "../responses/api.response";

@Injectable({
  providedIn: 'root'
})
export class CouponService {

  private apiBaseUrl = environment.apiBaseurl;

  constructor(private http: HttpClient) { }
  calculateCouponValue(couponCode: string, totalAmount: number): Observable<ApiResponse> {
    const url = `${this.apiBaseUrl}/coupons/calculate`;
    const params = new HttpParams()
      .set('couponCode', couponCode)
      .set('totalAmount', totalAmount.toString());

    return this.http.get<ApiResponse>(url, { params });
  }

}
