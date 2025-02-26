import {Component, OnInit} from '@angular/core';
import { RouterOutlet } from '@angular/router';
import {NgToastModule} from "ng-angular-popup";
import {NgxSpinnerModule, NgxSpinnerService} from "ngx-spinner";
import {SharedModule} from "./shared-module";
@Component({
  selector: 'app-root',
  standalone: true,
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
  imports: [RouterOutlet, NgToastModule,NgxSpinnerModule,SharedModule,]
})
export class AppComponent implements OnInit{
  title = 'my-app';
  constructor(private spinner: NgxSpinnerService) {}

  ngOnInit() {
    /** spinner starts on init */
    this.spinner.show();
    setTimeout(() => {
      /** spinner ends after 5 seconds */
      this.spinner.hide();
    }, 400);
  }
}

