import {Component, OnInit} from '@angular/core';
import {CommonModule, Location} from "@angular/common";
import {FormsModule} from "@angular/forms";
import {BaseChartDirective} from "ng2-charts";
import {Product} from "../../../models/product";
import {ProductService} from "../../../services/product.service";
import {Router} from "@angular/router";
import {Invoice} from "../../../models/Invoice";
import {invoiceService} from "../../../services/invoices.service";
import {HttpErrorResponse} from "@angular/common/http";
import {Category} from "../../../models/categogy";

@Component({
  selector: 'app-ocrinvoice',
  standalone: true,
  imports: [CommonModule,FormsModule,BaseChartDirective],
  templateUrl: './ocrinvoice.admin.component.html',
  styleUrl: './ocrinvoice.admin.component.scss'
})
export class OcrinvoiceAdminComponent implements OnInit{
  invoices: Invoice[] = [];
  selectedCategoryId: number  = 0; // Giá trị category được chọn
  currentPage: number = 0;
  itemsPerPage: number = 12;
  pages: number[] = [];
  totalPages:number = 0;
  visiblePages: number[] = [];
  keyword:string = "";
  localStorage?:Storage;
  isImageOpen = false;
  currentImage: string = '';




  constructor(private router:Router,private location:Location, private invoiceService: invoiceService
  ) {
    this.localStorage = document.defaultView?.localStorage;
  }
  ngOnInit(): void {
    this.getInvoiceData();
  }
  getInvoiceData(): void {
    this.invoiceService.getAllInvoices().subscribe({
      next: (apiResponse: any) => {
        debugger;
          this.invoices = apiResponse;  // Lưu trữ danh sách hóa đơn
          // this.totalPages = apiResponse.totalPages;  // Lưu tổng số trang

          // // Kiểm tra và tính toán các trang cần hiển thị
          // if (this.totalPages && this.currentPage !== undefined) {
          //   this.visiblePages = this.generateVisiblePageArray(this.currentPage, this.totalPages);
          // }

      },
      complete: () => {
        console.log('Request complete');
      },
      error: (error: HttpErrorResponse) => {
        console.error('Error fetching invoice data:', error?.error?.message ?? error.message);
      }
    });
  }
  deleteInvoice(invoice:Invoice) {
    const confirmation = window
      .confirm('Are you sure you want to delete this category?');
    if (confirmation) {
      debugger
      this.invoiceService.deleteInvoice(invoice.image_index).subscribe({
        next: (apiResponse: any) => {
          debugger
          console.error('Xóa thành công')
          location.reload();
        },
        complete: () => {
          debugger;
          location.reload();
        },
        error: (error: HttpErrorResponse) => {
          debugger;
          location.reload();
          console.error(error?.error?.message ?? '');
        }
      });
    }
  }

  searchProducts() {
    this.currentPage = 0;
    this.itemsPerPage = 12;
  }
  onPageChange(page: number) {
    debugger;
    this.currentPage = page < 0 ? 0 : page;
    this.localStorage?.setItem('currentProductAdminPage', String(this.currentPage));
  }


  generateVisiblePageArray(currentPage: number, totalPages: number): number[] {
    const maxVisiblePages = 5;
    const halfVisiblePages = Math.floor(maxVisiblePages / 2);

    let startPage = Math.max(currentPage - halfVisiblePages, 1);
    let endPage = Math.min(startPage + maxVisiblePages - 1, totalPages);

    if (endPage - startPage + 1 < maxVisiblePages) {
      startPage = Math.max(endPage - maxVisiblePages + 1, 1);
    }

    return new Array(endPage - startPage + 1).fill(0)
      .map((_, index) => startPage + index);
  }
  openImage(imageUrl: string): void {
    this.currentImage = imageUrl;  // Lưu URL của ảnh vào currentImage
    this.isImageOpen = true;       // Mở modal ảnh
  }

  closeImage(): void {
    this.isImageOpen = false;      // Đóng modal ảnh
  }

}
