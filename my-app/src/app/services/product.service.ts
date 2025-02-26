import {Injectable} from "@angular/core";
import {HttpClient, HttpParams} from "@angular/common/http";
import {Observable} from "rxjs";
import {Product} from '../models/product';
import {environment} from "../environments/environment";
import {ApiResponse} from "../responses/api.response";
import {InsertProductDTO} from "../dtos/product/insert.product.dto";
import {UpdateProductDTO} from "../dtos/product/update.product.dto";
@Injectable({
  providedIn:'root'
})
export class ProductService{
  private apiGetProducts = `${environment.apiBaseurl}/products`;
    constructor(private http:HttpClient) {}
  getProducts( keyword:string,categoryId:number,page:number,limit: number):Observable<Product[]>{
    const params = new HttpParams()

      .set('keyword', keyword)
      .set('category_id', categoryId)
      .set('page',page.toString())
      .set('limit',limit.toString())
      return this.http.get<Product[]>(this.apiGetProducts,{params});
  }
  getDetailProduct(productId: number) {
      debugger;
    return this.http.get(`${environment.apiBaseurl}/products/${productId}`);
  }
  getProductsByIds(productIds: number[]): Observable<Product[]> {
    // Chuyển danh sách ID thành một chuỗi và truyền vào params
    debugger
    const params = new HttpParams().set('ids', productIds.join(','));
    return this.http.get<Product[]>(`${this.apiGetProducts}/by-ids`, { params });
  }

  deleteProduct(productId: number): Observable<ApiResponse> {
    debugger
    return this.http.delete<ApiResponse>(`${this.apiGetProducts}/products/${productId}`);
  }
  updateProduct(productId: number, updatedProduct: UpdateProductDTO): Observable<any> {
    return this.http.put<any>(`${this.apiGetProducts}/products/${productId}`, updatedProduct);
  }
  insertProduct(insertProductDTO: InsertProductDTO): Observable<any> {
    // Add a new product
    return this.http.post<any>(`${this.apiGetProducts}/products`, insertProductDTO);
  }
  uploadImages(productId: number, files: File[]): Observable<ApiResponse> {
    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
      formData.append('files', files[i]);
    }
    // Upload images for the specified product id
    return this.http.post<ApiResponse>(`${this.apiGetProducts}/products/uploads/${productId}`, formData);
  }
  deleteProductImage(id: number): Observable<any> {
    debugger
    return this.http.delete<string>(`${this.apiGetProducts}/product_images/${id}`);
  }
}
