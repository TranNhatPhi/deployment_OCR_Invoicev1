import { Component } from '@angular/core';
import {FormBuilder, FormGroup, ReactiveFormsModule, Validators} from "@angular/forms";
import { HttpClient } from "@angular/common/http";
import { KeyValuePipe, NgForOf, NgIf } from "@angular/common";
import { invoiceService } from '../../services/invoices.service';
import { HeaderComponent } from "../header/header.component";
import { Invoice } from "../../models/Invoice";
import {NgxSpinnerService} from "ngx-spinner";
import {NgToastService} from "ng-angular-popup"; // Import service để gọi API

@Component({
  selector: 'app-ocr-user',
  standalone: true,
  imports: [
    NgIf,
    KeyValuePipe,
    NgForOf,
    HeaderComponent,
    ReactiveFormsModule,
  ],
  templateUrl: './ocr-user.component.html',
  styleUrls: ['./ocr-user.component.scss']  // Fix styleUrls (not styleUrl)
})
export class OCRUSERComponent  {
  invoices: Invoice[] = [];
  uploadForm: FormGroup;
  invoiceData: any;
  loading: boolean = false;
  imagePreviewUrl: string | ArrayBuffer | null = null; // Để lưu trữ đường dẫn ảnh preview

  constructor(private toast:NgToastService,private spinner: NgxSpinnerService,
    private fb: FormBuilder,
    private http: HttpClient,
    private invoiceService: invoiceService
  ) {
    this.uploadForm = this.fb.group({
      myfile: [null, Validators.required]
    });
  }

  // Phương thức để tạo URL đầy đủ từ đường dẫn cục bộ
  getImageUrl(imagePath: string): string {
    return <string>imagePath.split('/').pop();
  }

  // Hàm xử lý khi chọn tệp
  onFileChange(event: any) {
    const file = event.target.files[0];
    if (file) {
      this.uploadForm.patchValue({
        myfile: file
      });

      // Sử dụng FileReader để tạo ảnh preview
      const reader = new FileReader();
      reader.onload = (e: any) => {
        this.imagePreviewUrl = e.target.result; // Lưu trữ đường dẫn ảnh cho preview
      };
      reader.readAsDataURL(file); // Đọc file ảnh dưới dạng Data URL
    }
  }

  // Hàm gửi yêu cầu nhận diện hóa đơn
  onSubmit(): void {
    if (this.uploadForm.invalid) {
      return;
    }

    const formData = new FormData();
    const file = this.uploadForm.get('myfile')?.value;

    if (file) {
      formData.append('image', file, file.name); // Đảm bảo file là một đối tượng tệp có thuộc tính 'name'
    }

    this.loading = true;
    this.spinner.show();

    // Gọi API để nhận diện hóa đơn
    this.invoiceService.recognizeInvoice(formData).subscribe({
      next: (response: Invoice) => {
        this.loading = false;
        this.spinner.hide();
        this.toast.success("Nhận diện hóa đơn thành công!!!","Invoice",10000);
        this.invoiceData = response;  // Lưu trữ kết quả nhận diện
      },
      error: (error: any) => {
        this.loading = false;
        console.error('Lỗi nhận diện hóa đơn:', error);
        this.spinner.hide();
        this.toast.danger("lỗi URL hoặc file vui lòng chọn file ảnh","Crawl-Data",10000)
      },
      complete: () => {
        // Xử lý sau khi hoàn thành
        console.log('API nhận diện hóa đơn đã hoàn thành');

      }
    });
  }

  // Khai báo biến Array để sử dụng trong template
  protected readonly Array = Array;
}
