import {Component, OnInit} from '@angular/core';
import {Category} from "../../../models/categogy";
import {CategoryService} from "../../../services/category.service";
import {Router} from "@angular/router";
import {HttpErrorResponse} from "@angular/common/http";
import {ApiResponse} from "../../../responses/api.response";
import {FormsModule} from "@angular/forms";
import {CommonModule} from "@angular/common";
import {BaseChartDirective} from "ng2-charts";
import {ChartDataset, ChartOptions} from "chart.js";

@Component({
  selector: 'app-category-admin',
  standalone: true,
  imports: [CommonModule,FormsModule,BaseChartDirective],
  templateUrl: './category.admin.component.html',
  styleUrl: './category.admin.component.scss'
})
export class CategoryAdminComponent implements OnInit{

  categories: Category[] = []; // Dữ liệu động từ categoryService
  constructor(
    private categoryService: CategoryService,
    private router: Router,
  ) {}
  public pieChartOptions: ChartOptions<'pie'> = {
    responsive: false,
  };
  public pieChartLabels: string[] =  [ 'Download', 'Sales' ,  'In', 'Store', 'Sales' , 'Mail Sales' ];
  public pieChartDatasets: ChartDataset<'pie'>[] = [{
    data: [] as number[],
    backgroundColor: [''] as string[], // Add backgroundColor property
    borderColor: [] as string[], // Add borderColor property
    borderWidth: 1
  }];
  public pieChartLegend = true;
  public pieChartPlugins = [];
  ngOnInit() {
    this.getCategories(0, 100);
  }
  getCategories(page: number, limit: number) {
    this.categoryService.getCategories(page, limit).subscribe({
      next: (apiResponse: any) => {
        debugger;
        this.categories = apiResponse;
      },
      complete: () => {
        this.updateChart();
        debugger;
      },
      error: (error: HttpErrorResponse) => {
        debugger;
        console.error(error?.error?.message ?? '');
      }
    });
  }
 /* private updateChart(): void {
    this.pieChartLabels = this.categories.map(category => category.name); // Adjust according to your Category model
    this.pieChartDatasets[0].data = this.categories.map(category => category.id); // Adjust according to your Category model

    // Set colors for the chart segments
    const backgroundColors = [
      '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'
    ]; // Add more colors if needed

    this.pieChartDatasets[0].backgroundColor = backgroundColors.slice(0, this.categories.length);
    this.pieChartDatasets[0].borderColor = backgroundColors.slice(0, this.categories.length);
  }*/
  private updateChart(): void {
    this.pieChartLabels = this.categories.map(category => category.name); // Adjust according to your Category model
    this.pieChartDatasets[0].data = this.categories.map(category => category.id); // Adjust according to your Category model

    // Generate random colors for the chart segments based on the number of categories
    const generateRandomColor = () => {
      const letters = '0123456789ABCDEF';
      let color = '#';
      for (let i = 0; i < 6; i++) { // Hex color is always 6 characters long
        color += letters[Math.floor(Math.random() * 16)];
      }
      return color;
    };

    this.pieChartDatasets[0].backgroundColor = this.categories.map(() => generateRandomColor());
    this.pieChartDatasets[0].borderColor = this.categories.map(() => '#FFFFFF'); // You can change the border color if needed
  }

  insertCategory() {
    debugger
    // Điều hướng đến trang detail-category với categoryId là tham số
    this.router.navigate(['/admin/categories/insert']);
    this.updateChart();
  }

  // Hàm xử lý sự kiện khi sản phẩm được bấm vào
  updateCategory(categoryId: number) {
    debugger
    this.router.navigate(['/admin/categories/update', categoryId]);
    this.updateChart();
  }
  deleteCategory(category: Category) {
    const confirmation = window
      .confirm('Are you sure you want to delete this category?');
    if (confirmation) {
      debugger
      this.categoryService.deleteCategory(category.id).subscribe({
        next: (apiResponse: any) => {
          debugger
          console.error('Xóa thành công')
          location.reload();
        },
        complete: () => {
          debugger;
          this.updateChart();
        },
        error: (error: HttpErrorResponse) => {
          debugger;
          console.error(error?.error?.message ?? '');
        }
      });
    }
  }

}
