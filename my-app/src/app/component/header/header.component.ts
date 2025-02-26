import {Component, OnInit} from '@angular/core';
import {  BsModalService } from 'ngx-bootstrap/modal';
import { SharedModule } from "../../shared-module";
import { LoginComponent } from "../login/login.component";
import { ChatComponent } from '../chat/chat.component';
import {Router, RouterLink} from "@angular/router";
import {TokenService} from "../../services/token.service";
import {UserService} from "../../services/user.service";
import {UserResponse} from "../../responses/user/user.response";
import {NgbPopover} from "@ng-bootstrap/ng-bootstrap";
import {CartService} from "../../services/cart.service";

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [SharedModule, ChatComponent, RouterLink, NgbPopover],
  templateUrl: './header.component.html',
  styleUrl: './header.component.scss'
})
export class HeaderComponent implements OnInit{
  currentUser: any;
  userResponse?:UserResponse | null;
  isPopoverOpen = false;
  activeNavItem: number = 0;

  togglePopover(event: Event): void {
    event.preventDefault();
    this.isPopoverOpen = !this.isPopoverOpen;
  }

  handleItemClick(index: number): void {
    //alert(`Clicked on "${index}"`);
    if(index === 0) {
      debugger
      this.router.navigate(['/user-profile']).then(()=>{
        console.log('truy cập thành công');
      } );
    } else if (index === 2) {
      this.userService.removeUserFromLocalStorage();
      this.tokenService.removeToken();
      this.cartService.clearCart();
      this.userResponse = this.userService.getUserResponseFromLocalStorage();
    }
    else{
    }
    this.isPopoverOpen = false; // Close the popover after clicking an item
  }

  constructor(
    private cartService:CartService,
    private userService: UserService,
    private tokenService: TokenService,
    private bsModal: BsModalService,
    private router:Router
  ) {}
  ngOnInit() {
    this.userResponse = this.userService.getUserResponseFromLocalStorage();
  }
  setActiveNavItem(index: number) {
    this.activeNavItem = index;
  }

  openformlogin() {
    this.bsModal.show(LoginComponent, {
    })
  }
}
