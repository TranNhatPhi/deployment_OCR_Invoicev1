import {Injectable} from "@angular/core";
import {environment} from "../environments/environment";
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Observable} from "rxjs";
import {Invoice} from "../models/Invoice";

@Injectable({

  providedIn: 'root',
})
export class invoiceService {
  private apiUrl = `${environment.apiBaseurl}/invoices/upload-image`;
  private apiUrlGet = `${environment.apiBaseurl}/invoices`;
  constructor(private http: HttpClient) {}

  recognizeInvoice(formData: FormData): Observable<Invoice> {
    return this.http.post<Invoice>(this.apiUrl, formData);
  }
  getAllInvoices(): Observable<any> {
    return this.http.get<any>(this.apiUrlGet);
  }
  deleteInvoice(id: number): Observable<string> {
    debugger
    return this.http.delete(`${this.apiUrlGet}/${id}`, {
      responseType: 'text',
    });
  }
}
