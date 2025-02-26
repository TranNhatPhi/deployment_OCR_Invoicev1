import {Component, inject} from '@angular/core';
import {FormsModule} from '@angular/forms';
import {GeminiService} from '../../gemini.service';
import {CommonModule} from '@angular/common';
import {HeaderComponent} from '../header/header.component';

@Component({
  selector: 'app-aigemini',
  standalone: true,
  imports: [FormsModule, CommonModule, HeaderComponent],
  templateUrl: './aigemini.component.html',
  styleUrl: './aigemini.component.scss'
})
export class AigeminiComponent {
  title = 'gemini-inte';

  prompt: string = '';
  geminiService: GeminiService = inject(GeminiService);

  loading: boolean = false;

  chatHistory: any[] = [];
  constructor() {
    this.geminiService.getMessageHistory().subscribe((res) => {
      if (res) {
        this.chatHistory.push(res);
      }
    })
  }

  async sendData() {
    if (this.prompt) {
      this.loading = true;
      const data = this.prompt;
      this.prompt = '';
      await this.geminiService.generateText(data);
      this.loading = false;
    }
  }

  formatText(text: string) {
    return text.replaceAll('*', '');
  }
}
