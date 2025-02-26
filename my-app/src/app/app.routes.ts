import {Routes} from '@angular/router';
import {HomeComponent} from './component/home/home.component';
import {OrderConfirmComponent} from './component/order-confirm/order-confirm.component';
import {LoginComponent} from './component/login/login.component';
import {RegisterComponent} from './component/register/register.component';
import {DetailProductComponent} from './component/detail-product/detail-product.component';
import {ContactComponent} from './component/contact/ContactComponent';
import {ChatComponent} from './component/chat/chat.component';
import {AuthGuardFn} from "./component/guards/auth.guard";
import {UserProfileComponent} from "./component/user-profile/user-profile.component";
import {AdminComponent} from "./component/admin/admin.component";
import {AdminGuardFn} from "./component/guards/admin.guard";
import {OrdersAdminComponent} from "./component/admin/orders/orders.admin.component";
import {OrderComponent} from "./component/order/order.component";
import {ThankYouComponent} from "./component/thank-you/thank-you.component";
import {CategoryAdminComponent} from "./component/admin/category/category.admin.component";
import {AigeminiComponent} from "./component/aigemini/aigemini.component";
import {InsertCategoryAdminComponent} from "./component/admin/category/insert/insert.category.admin.component";
import {UpdateCategoryAdminComponent} from "./component/admin/category/update/update.category.admin.component";
import {CrawlsDataAdminComponent} from "./component/admin/crawls-data/crawls-data.admin.component";
import {DetailOrderAdminComponent} from "./component/admin/detail-order/detail-order.admin.component";
import {UserAdminComponent} from "./component/admin/user/user.admin.component";
import {ProductAdminComponent} from "./component/admin/product/product.admin.component";
import {OcrinvoiceAdminComponent} from "./component/admin/ocrinvoice/ocrinvoice.admin.component";
import {OCRUSERComponent} from "./component/ocr-user/ocr-user.component";


export const routes: Routes = [
  /*{path:'',loadComponent:()=>import('./component/login/login.component').then(a=>a.LoginComponent)},*/
  {
    path: '',
    redirectTo: 'home',
    pathMatch: 'full'
  }, {
    path: 'home',
    component: HomeComponent
  }, {
    path: 'admin',
    component: AdminComponent,
    canActivate:[AdminGuardFn]
  }, {
    path: 'admin',
    component: AdminComponent,
    canActivate:[AdminGuardFn],
    children: [
      {
        path: 'categories',
        component: CategoryAdminComponent
      },
      {
        path: 'products',
        component: ProductAdminComponent
      },
      {
        path: 'orders',
        component: OrdersAdminComponent

      },

      //sub path
       {
         path: 'orders/:id',
         component: DetailOrderAdminComponent
       },
       /*{
         path: 'products/update/:id',
         component: UpdateProductAdminComponent
       },
       {
         path: 'products/insert',
         component: InsertProductAdminComponent
       },*/
      {
        path: 'crawlsData',
        component: CrawlsDataAdminComponent
      },
      {
        path: 'invoices',
        component:OcrinvoiceAdminComponent
      },
       //categories
       {
         path: 'categories/update/:id',
         component: UpdateCategoryAdminComponent
       },
       {
         path: 'categories/insert',
         component: InsertCategoryAdminComponent
       },
       {
         path: 'users',
         component: UserAdminComponent
       },
    ]
  },
  {
    path: 'user-profile',
    component: UserProfileComponent,
    canActivate:[AuthGuardFn] },
  {
    path: 'my-orders',
    component: OrderConfirmComponent
  },
  {
    path: 'login',
    component: LoginComponent
  }, {
    path: 'register',
    component: RegisterComponent
  }, {
    path: 'products/:id',
    component: DetailProductComponent
  }, { path: 'orders/:id',
    component: OrderConfirmComponent
  },   { path: 'orders', component: OrderComponent,canActivate:[AuthGuardFn] },
  { path: 'thanhtoansuccess', component: ThankYouComponent,canActivate:[AuthGuardFn] },
  {
    path: 'contact',
    component: ContactComponent
  },{
    path: 'ocr',
    component: OCRUSERComponent
  }, {
    path: 'chatgpt',
    component: ChatComponent
  }, {
    path: 'aigemini',
    component: AigeminiComponent
  }/*, {
    path: 'browse',
    loadComponent: () => import('./component/browse/browse.component').then(a => a.BrowseComponent)
  }*/
];
