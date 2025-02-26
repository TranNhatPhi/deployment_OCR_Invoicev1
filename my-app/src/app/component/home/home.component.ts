import {Component, OnInit} from '@angular/core';
import { FooterComponent } from '../footer/footer.component';
import { HeaderComponent } from '../header/header.component';
import { GoogleSearchComponent } from '../google-search/google-search.component';
import {ProductService} from "../../services/product.service";
import {Product} from "../../models/product";
import {NgClass, NgForOf, NgIf} from "@angular/common";
import { Router } from '@angular/router';
import {ChatComponent} from "../chat/chat.component";
import {FormsModule} from "@angular/forms";
import {Category} from "../../models/categogy";
import {CategoryService} from "../../services/category.service";
import {SharedModule} from "../../shared-module";
import {HttpErrorResponse} from "@angular/common/http";
import {ChatbotComponent} from "../chatbot/chatbot.component";
import {NgToastService} from "ng-angular-popup";


@Component({
  selector: 'app-home',
  standalone: true,
  imports: [ChatbotComponent,SharedModule,FooterComponent, HeaderComponent, GoogleSearchComponent, NgClass, NgIf, NgForOf, ChatComponent, FormsModule],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent implements OnInit{
  products:Product[]=[];
  currentPage:number=1;
  itemsPerPage:number=12;
  categories: Category[] = [];
  totalPages:number=0;
  visiblePages:number[]=[];
  keyword:string = "";
  selectedCategoryId:number=0;
  showChat:boolean=false;
  constructor(private toast:NgToastService,private productService:ProductService,private categoryService:CategoryService,private router: Router) {}
  ngOnInit() {

    this.getProducts(this.keyword,this.selectedCategoryId,this.currentPage,this.itemsPerPage);
    this.getCategories(1,100);
  }
  toggleChat() {
    this.showChat = !this.showChat;
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
  searchProducts(){
    this.currentPage=1;
    this.itemsPerPage=12;
    debugger;
    this.getProducts(this.keyword,this.selectedCategoryId,this.currentPage,this.itemsPerPage);
    this.toast.success("Tìm kiếm thành công!!!","Login",3000);
  }
  getProducts(keyword:string,selectedCategoryId:number, page:number ,limit: number){
    this.productService.getProducts(keyword,selectedCategoryId,page,limit).subscribe({
      next:(response:any)=>{
        debugger;
        response.products.forEach((product:Product)=>{
          product.url=product.thumbnail;
        });
        this.products=response.products;
        this.totalPages = response.totalPages;
        this.visiblePages = this.generateVisiblePageArray(this.currentPage,this.itemsPerPage);
      },
      complete: ()=> {
        debugger;
      },
      error: (error: any) => {
        debugger;
        console.error('Error fetching products:',error);
      },

    });
  }
  onPageChange(page: number) {
    debugger;
    this.currentPage = page;
    this.getProducts(this.keyword, this.selectedCategoryId, this.currentPage, this.itemsPerPage);
  }

  generateVisiblePageArray(currentPage: number, totalPages: number): number[] {
    const maxVisiblePages = 5;
    const halfVisiblePages = Math.floor(maxVisiblePages / 2);

    let startPage = Math.max(currentPage - halfVisiblePages, 1);
    let endPage = Math.min(startPage + maxVisiblePages - 1, totalPages);

    if (endPage - startPage + 1 < maxVisiblePages) {
      startPage = Math.max(endPage - maxVisiblePages + 1, 1);
    }

    return new Array(endPage - startPage + 1).fill(0).map((_, index) => startPage + index);
  }
  onProductClick(productId: number) {
    debugger
    // Điều hướng đến trang detail-product với productId là tham số

    this.router.navigate(['/products', productId]).then(() => {
      console.log('Navigation ended successfully');
    }).catch((error) => {
      console.error('Navigation error:', error);
    });
  }
}
