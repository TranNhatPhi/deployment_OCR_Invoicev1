import {Component, OnInit} from '@angular/core';
import {NgForOf} from "@angular/common";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {Category} from "../../../models/categogy";
import {CategoryService} from "../../../services/category.service";
import {HttpErrorResponse} from "@angular/common/http";
import {CrawlsDataService} from "../../../services/crawls-data.service";
import {NgxSpinnerComponent, NgxSpinnerService} from "ngx-spinner";
import {NgToastService} from "ng-angular-popup";

@Component({
  selector: 'app-crawls-data-admin',
  standalone: true,
  imports: [
    NgForOf,
    ReactiveFormsModule,
    FormsModule,
    NgxSpinnerComponent
  ],
  templateUrl: './crawls-data.admin.component.html',
  styleUrl: './crawls-data.admin.component.scss'
})
export class CrawlsDataAdminComponent implements OnInit{
  categories: Category[] = [];

  param = {
    url: '',
    categoryId1: ''
  }
  formData: FormData = new FormData();
 /* crawlsDataDto:CrawlsDataDto = {
    url:'',
    cateId:0
  }*/
  constructor(private toast:NgToastService,private spinner: NgxSpinnerService,private categoryService:CategoryService,private crawlDataService:CrawlsDataService) {
  }
  ngOnInit(){
    this.getCategories(1,100);
  }

  fucCrawlData(){
    debugger
    this.spinner.show();
    this.formData = new FormData();
    this.formData.append('url', this.param.url);
    this.formData.append('categoryId1', this.param.categoryId1);

    this.crawlDataService.apiCrawlData(this.formData).subscribe({
      next: (apiResponse: any) => {
        console.log('API response:', apiResponse);
        this.spinner.hide();
        this.toast.success("Thu thập dữ liệu thành công!!!","Crawl-Data",10000);
      },
      complete: () => {
        console.log('API call completed');
        this.spinner.hide();
      },
      error: (error: HttpErrorResponse) => {
        console.error('Error:', error);
        this.spinner.hide();
        this.toast.danger("lỗi URL hoặc loại sản phẩm","Crawl-Data",50000);
      }
    });
  }

  getCategories(page: number, limit: number) {
    this.categoryService.getCategories(page, limit).subscribe({
      next: (apiResponse: any) => {
        debugger;
        this.categories = apiResponse;

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
