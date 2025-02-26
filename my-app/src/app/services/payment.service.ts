import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import {environment} from "../environments/environment";

@Injectable({
  providedIn: 'root'
})
export class PaymentService {

  private apiPrefix = environment.apiBaseurl; // Ensure this is defined in your environment files

  constructor(private http: HttpClient) { }

  initiatePayment(paymentData: any): Observable<any> {
    return this.http.post(`${this.apiPrefix}/payment/vnpay`, paymentData);
  }
}
