import {Component, OnInit} from '@angular/core';
import {Product} from "../../../../models/product";
import {Category} from "../../../../models/categogy";
import {ProductService} from "../../../../services/product.service";
import {ActivatedRoute, Router} from "@angular/router";
import {CategoryService} from "../../../../services/category.service";
import {Location} from "@angular/common";
import {ApiResponse} from "../../../../responses/api.response";
import {HttpErrorResponse} from "@angular/common/http";
import {ProductImage} from "../../../../models/product.image";
import {UpdateProductDTO} from "../../../../dtos/product/update.product.dto";
import {FormsModule} from "@angular/forms";

@Component({
  selector: 'app-update.product.admin',
  standalone: true,
  imports: [
    FormsModule
  ],
  templateUrl: './update.product.admin.component.html',
  styleUrl: './update.product.admin.component.scss'
})
export class UpdateProductAdminComponent implements OnInit{

  productId: number;
  product: Product;
  updatedProduct: Product;
  categories: Category[] = []; // Dữ liệu động từ categoryService
  currentImageIndex: number = 0;
  images: File[] = [];

  constructor(
    private productService: ProductService,
    private route: ActivatedRoute,
    private router: Router,
    private categoryService: CategoryService,
    private location: Location,
  ) {
    this.productId = 0;
    this.product = {} as Product;
    this.updatedProduct = {} as Product;
  }

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      this.productId = Number(params.get('id'));
      this.getProductDetails();
    });
    this.getCategories(1, 100);
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
  getProductDetails(): void {
    this.productService.getDetailProduct(this.productId).subscribe({
      next: (apiResponse: any) => {

        this.product = apiResponse.products;
        this.updatedProduct = { ...apiResponse };

      },
      complete: () => {

      },
      error: (error: HttpErrorResponse) => {
        debugger;
        console.error(error?.error?.message ?? '');
      }
    });
  }
  updateProduct() {
    // Implement your update logic here
    const updateProductDTO: UpdateProductDTO = {
      name: this.updatedProduct.name,
      price: this.updatedProduct.price,
      description: this.updatedProduct.description,
      category_id: this.updatedProduct.category_id
    };
    this.productService.updateProduct(this.product.id, updateProductDTO).subscribe({
      next: (apiResponse: ApiResponse) => {
        debugger
      },
      complete: () => {
        debugger;
        this.router.navigate(['/admin/products']);
      },
      error: (error: HttpErrorResponse) => {
        debugger;
        console.error(error?.error?.message ?? '');
      }
    });
  }
  showImage(index: number): void {
    debugger
    if (this.product && this.product.product_images &&
      this.product.product_images.length > 0) {
      // Đảm bảo index nằm trong khoảng hợp lệ
      if (index < 0) {
        index = 0;
      } else if (index >= this.product.product_images.length) {
        index = this.product.product_images.length - 1;
      }
      // Gán index hiện tại và cập nhật ảnh hiển thị
      this.currentImageIndex = index;
    }
  }
  thumbnailClick(index: number) {
    debugger
    // Gọi khi một thumbnail được bấm
    this.currentImageIndex = index; // Cập nhật currentImageIndex
  }
  nextImage(): void {
    debugger
    this.showImage(this.currentImageIndex + 1);
  }

  previousImage(): void {
    debugger
    this.showImage(this.currentImageIndex - 1);
  }
  onFileChange(event: any) {
    // Retrieve selected files from input element
    const files = event.target.files;
    // Limit the number of selected files to 5
    if (files.length > 5) {
      console.error('Please select a maximum of 5 images.');
      return;
    }
    // Store the selected files in the newProduct object
    this.images = files;
    this.productService.uploadImages(this.productId, this.images).subscribe({
      next: (apiResponse: ApiResponse) => {
        debugger
        // Handle the uploaded images response if needed
        console.log('Images uploaded successfully:', apiResponse);
        this.images = [];
        // Reload product details to reflect the new images
        this.getProductDetails();
      },
      error: (error: HttpErrorResponse) => {
        debugger;
        console.error(error?.error?.message ?? '');
      }
    })
  }
  deleteImage(productImage: ProductImage) {
    if (confirm('Are you sure you want to remove this image?')) {
      // Call the removeImage() method to remove the image
      this.productService.deleteProductImage(productImage.id).subscribe({
        next:(productImage: ProductImage) => {
          location.reload();
        },
        error: (error: HttpErrorResponse) => {
          debugger;
          console.error(error?.error?.message ?? '');
        }
      });
    }
  }
}

