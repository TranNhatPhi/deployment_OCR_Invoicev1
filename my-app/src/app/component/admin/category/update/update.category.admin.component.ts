import {Component, OnInit} from '@angular/core';
import {FormsModule} from "@angular/forms";
import {Category} from "../../../../models/categogy";
import {CategoryService} from "../../../../services/category.service";
import {ActivatedRoute, Router} from "@angular/router";
import {HttpErrorResponse} from "@angular/common/http";
import {ApiResponse} from "../../../../responses/api.response";
import {UpdateCategoryDTO} from "../../../../dtos/category/update.category.dto";

@Component({
  selector: 'app-update',
  standalone: true,
  imports: [
    FormsModule
  ],
  templateUrl: './update.category.admin.component.html',
  styleUrl: './update.category.admin.component.scss'
})
export class UpdateCategoryAdminComponent implements OnInit {
  categoryId: number;
  updatedCategory: Category;

  constructor(
    private categoryService: CategoryService,
    private route: ActivatedRoute,
    private router: Router,

  ) {
    this.categoryId = 0;
    this.updatedCategory = {} as Category;
  }

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      debugger
      this.categoryId = Number(params.get('id'));
      this.getCategoryDetails();
    });

  }

  getCategoryDetails(): void {
    this.categoryService.getDetailCategory(this.categoryId).subscribe({
      next: (apiResponse: any) => {
        this.updatedCategory = apiResponse;
      },
      complete: () => {

      },
      error: (error: HttpErrorResponse) => {
        debugger;
        console.error(error?.error?.message ?? '');
      }
    });
  }
  updateCategory() {
    // Implement your update logic here
    const updateCategoryDTO: UpdateCategoryDTO = {
      name: this.updatedCategory.name,
    };
    this.categoryService.updateCategory(this.categoryId, updateCategoryDTO).subscribe({
      next: (response: any) => {
        debugger
      },
      complete: () => {
        debugger;
        this.router.navigate(['/admin/categories']);
      },
      error: (error: HttpErrorResponse) => {
        debugger;
        console.error(error?.error?.message ?? '');
      }
    });
  }
}

