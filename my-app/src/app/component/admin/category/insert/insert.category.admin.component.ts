import {Component, OnInit} from '@angular/core';
import {FormsModule} from "@angular/forms";
import {Category} from "../../../../models/categogy";
import {ActivatedRoute, Router} from "@angular/router";
import {CategoryService} from "../../../../services/category.service";
import {ProductService} from "../../../../services/product.service";
import {InsertCategoryDTO} from "../../../../dtos/category/insert.category.dto";
import {HttpErrorResponse} from "@angular/common/http";

@Component({
  selector: 'app-insert',
  standalone: true,
  imports: [
    FormsModule
  ],
  templateUrl: './insert.category.admin.component.html',
  styleUrl: './insert.category.admin.component.scss'
})
export class InsertCategoryAdminComponent implements OnInit {
  insertCategoryDTO: InsertCategoryDTO = {
    name: '',
  };
  categories: Category[] = []; // Dữ liệu động từ categoryService
  constructor(
    private router: Router,
    private categoryService: CategoryService,
  ) {

  }
  ngOnInit() {

  }

  insertCategory() {
    debugger
    this.categoryService.insertCategory(this.insertCategoryDTO).subscribe({
      next: (response) => {
        debugger
        this.router.navigate(['/admin/categories']).then(() =>{
          alert("thêm 1 loại sản phẩm thành công");
        } );
      },
      error: (error: HttpErrorResponse) => {
        debugger;
        console.error(error.error);
      }
    });
  }
}

