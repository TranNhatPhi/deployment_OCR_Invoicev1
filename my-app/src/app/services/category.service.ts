import {environment} from "../environments/environment";
import {HttpClient, HttpParams} from "@angular/common/http";
import {Observable} from "rxjs";
import {Injectable} from "@angular/core";
import {ApiResponse} from "../responses/api.response";
import {InsertCategoryDTO} from "../dtos/category/insert.category.dto";
import {UpdateCategoryDTO} from "../dtos/category/update.category.dto";
import {Product} from "../models/product";

@Injectable({
  providedIn: 'root'
})
export class CategoryService {
  private apiGetCategories  = `${environment.apiBaseurl}/categories`;

  constructor(private http: HttpClient) { }
  getCategories(page: number, limit: number):Observable<ApiResponse> {
    const params = new HttpParams()
      .set('page', page.toString())
      .set('limit', limit.toString());
    return this.http.get<ApiResponse>(`${environment.apiBaseurl}/categories`, { params });
  }
  getProducts(): Observable<Product[]> {
    return this.http.get<Product[]>(`${environment.apiBaseurl}/products`);
  }
  getDetailCategory(id: number): Observable<ApiResponse> {
    return this.http.get<ApiResponse>(`${environment.apiBaseurl}/categories/${id}`);
  }
  deleteCategory(id: number): Observable<string> {
    debugger
    return this.http.delete(`${environment.apiBaseurl}/categories/${id}`, {
      responseType: 'text',
    });
  }
  updateCategory(id: number, updatedCategory: UpdateCategoryDTO): Observable<ApiResponse> {
    return this.http.put<ApiResponse>(`${environment.apiBaseurl}/categories/${id}`, updatedCategory);
  }
  insertCategory(insertCategoryDTO: InsertCategoryDTO): Observable<ApiResponse> {
    // Add a new category
    return this.http.post<ApiResponse>(`${environment.apiBaseurl}/categories`, insertCategoryDTO);
  }
}
