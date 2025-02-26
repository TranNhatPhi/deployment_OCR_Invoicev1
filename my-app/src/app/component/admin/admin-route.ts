import {AdminComponent} from "./admin.component";
import {OrdersAdminComponent} from "./orders/orders.admin.component";
import {CategoryAdminComponent} from "./category/category.admin.component";
import {Routes} from "@angular/router";
import {ProductAdminComponent} from "./product/product.admin.component";
import {OcrinvoiceAdminComponent} from "./ocrinvoice/ocrinvoice.admin.component";

export const adminRoutes: Routes = [
  {
    path: 'admin',
    component: AdminComponent,
    children: [
      {
        path: 'orders',
        component: OrdersAdminComponent
      },
      {
        path: 'products',
        component: ProductAdminComponent
      },

      {
        path: 'categories',
        component: CategoryAdminComponent
      },
      {
        path: 'crawlsData',
        component: CategoryAdminComponent
      },
      {
        path:'invoices',
        component:OcrinvoiceAdminComponent
      },
     /* //sub path
      {
        path: 'orders/:id',
        component: DetailOrderAdminComponent
      },
      {
        path: 'products/update/:id',
        component: UpdateProductAdminComponent
      },
      {
        path: 'products/insert',
        component: InsertProductAdminComponent
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
      },*/
    ]
  }
];
/*
@NgModule({
    imports: [
        RouterModule.forChild(routes)
    ],
    exports: [RouterModule]
})
export class AdminRoutingModule { }
*/
