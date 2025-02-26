import {Component, Inject, inject, OnInit} from '@angular/core';
import {DOCUMENT, NgClass} from "@angular/common";
import {UserService} from "../../../services/user.service";
import {ActivatedRoute, Router} from "@angular/router";
import {UserResponse} from "../../../responses/user/user.response";
import {HttpErrorResponse} from "@angular/common/http";

@Component({
  selector: 'app-user',
  standalone: true,
  imports: [
    NgClass
  ],
  templateUrl: './user.admin.component.html',
  styleUrl: './user.admin.component.scss'
})
export class UserAdminComponent implements OnInit{
  userService = inject(UserService);
  router = inject(Router)
  route = inject(ActivatedRoute);
  users: UserResponse[] = [];
  currentPage: number = 0;
  itemsPerPage: number = 12;
  pages: number[] = [];
  totalPages:number = 0;
  visiblePages: number[] = [];
  keyword:string = "";
  localStorage?:Storage;

  constructor(
    //private location: Location,
    @Inject(DOCUMENT) private document: Document
  ) {
    this.localStorage = document.defaultView?.localStorage;
  }
  ngOnInit(): void {
    this.currentPage = Number(this.localStorage?.getItem('currentUserAdminPage')) || 0;
    this.getUsers(this.keyword, this.currentPage, this.itemsPerPage);
  }

  searchUsers() {
    this.currentPage = 0;
    this.itemsPerPage = 12;
    this.getUsers(this.keyword.trim(), this.currentPage, this.itemsPerPage);
  }

  getUsers(keyword: string, page: number, limit: number) {
    this.userService.getUsers({ keyword, page, limit }).subscribe({
      next: (apiResponse: any) => {
        debugger
        const response = apiResponse.data;
        this.users = response.users;
        this.totalPages = response.totalPages;
        this.visiblePages = this.generateVisiblePageArray(this.currentPage, this.totalPages);
      },
      complete: () => {
        // Handle complete event
        debugger
      },
      error: (error: HttpErrorResponse) => {
        debugger;
        console.error(error?.error?.message ?? '');
      }
    });
  }

  onPageChange(page: number) {
    this.currentPage = page < 0 ? 0 : page;
    this.localStorage?.setItem('currentUserAdminPage', String(this.currentPage));
    this.getUsers(this.keyword, this.currentPage, this.itemsPerPage);
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

  // Hàm xử lý sự kiện khi thêm mới sản phẩm
  insertUser() {
    debugger
    // Điều hướng đến trang detail-user với userId là tham số
    this.router.navigate(['/admin/users/insert']);
  }

  // Hàm xử lý sự kiện khi sản phẩm được bấm vào
  updateUser(userId: number) {
    debugger
    // Điều hướng đến trang detail-user với userId là tham số
    this.router.navigate(['/admin/users/update', userId]);
  }
  resetPassword(userId: number) {
    this.userService.resetPassword(userId).subscribe({
      next: (apiResponse: any) => {
        console.error('Block/unblock user successfully');
        //location.reload();
      },
      complete: () => {
        // Handle complete event
      },
      error: (error: HttpErrorResponse) => {
        debugger;
        console.error(error?.error?.message ?? '');
      }
    });
  }

  toggleUserStatus(user: UserResponse) {
    let confirmation: boolean;
    if (user.is_active) {
      confirmation = window.confirm('Are you sure you want to block this user?');
    } else {
      confirmation = window.confirm('Are you sure you want to enable this user?');
    }

    if (confirmation) {
      const params = {
        userId: user.id,
        enable: !user.is_active
      };

      this.userService.toggleUserStatus(params).subscribe({
        next: (response: any) => {
          console.error('Block/unblock user successfully');
          location.reload();
        },
        complete: () => {
          // Handle complete event
        },
        error: (error: HttpErrorResponse) => {
          debugger;
          console.error(error?.error?.message ?? '');
        }
      });
    }
  }
}
