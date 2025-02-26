import {Component, inject, OnInit} from '@angular/core';
import {UserResponse} from "../../responses/user/user.response";
import {TokenService} from "../../services/token.service";
import {Router, RouterLink, RouterLinkActive, RouterOutlet} from "@angular/router";
import {UserService} from "../../services/user.service";
import {LayoutComponent} from "./layout/layout.component";
import {NgSwitch, NgSwitchCase} from "@angular/common";
import {OrdersAdminComponent} from "./orders/orders.admin.component";

@Component({
  selector: 'app-admin',
  standalone: true,
  imports: [LayoutComponent, NgSwitch, NgSwitchCase, OrdersAdminComponent, RouterLink, RouterLinkActive, RouterOutlet],
  templateUrl: './admin.component.html',
  styleUrl: './admin.component.scss'
})
export class AdminComponent implements OnInit{
  //adminComponent: string = 'orders';
  userResponse?:UserResponse | null;
  private userService = inject(UserService);
  private tokenService = inject(TokenService);
  private router = inject(Router);

  ngOnInit() {
    this.userResponse = this.userService.getUserResponseFromLocalStorage();
    // Default router
    debugger
    if (this.router.url === '/admin') {
      this.router.navigate(['/admin/categories']);
    }
  }
  logout() {
    this.userService.removeUserFromLocalStorage();
    this.tokenService.removeToken();
    this.userResponse = this.userService.getUserResponseFromLocalStorage();
    this.router.navigate(['/']);
  }
  showAdminComponent(componentName: string): void {
    debugger
    if (componentName === 'categories') {
      this.router.navigate(['/admin/categories']);
    } else if (componentName === 'orders') {
      this.router.navigate(['/admin/orders']);
    } else if (componentName === 'products') {
      this.router.navigate(['/admin/products']);
    } else if (componentName === 'users') {
      this.router.navigate(['/admin/users']);
    }else if (componentName === 'CrawlsData') {
      this.router.navigate(['/admin/crawlsData']);
    }else if (componentName === 'ocrinvoice'){
      this.router.navigate(['/admin/invoices'])
    }
  }
}

