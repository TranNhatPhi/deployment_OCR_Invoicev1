
import { Component, OnInit, Renderer2 } from '@angular/core';

@Component({
  standalone: true,
  imports: [],
  templateUrl: './google-search.component.html',
  selector: 'app-google-search',
  styleUrls: ['./google-search.component.scss']
})
export class GoogleSearchComponent implements OnInit {
  constructor(private renderer: Renderer2) { }

  ngOnInit(): void {
    // Tạo script tag và thêm vào DOM
    const script = this.renderer.createElement('script');
    this.renderer.setAttribute(script, 'async', 'true');
    this.renderer.setAttribute(script, 'src', 'https://cse.google.com/cse.js?cx=950617e11def34182');
    this.renderer.appendChild(document.body, script);
  }
}
