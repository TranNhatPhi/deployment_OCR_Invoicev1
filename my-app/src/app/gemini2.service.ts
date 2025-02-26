import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import {BehaviorSubject, Observable} from 'rxjs';
import {GoogleGenerativeAI} from "@google/generative-ai";

@Injectable({
  providedIn: 'root'
})
export class Gemini2Service {
  private generativeAI: GoogleGenerativeAI;
  private messageHistory: BehaviorSubject<any> = new BehaviorSubject(null);

  constructor() {
    this.generativeAI = new GoogleGenerativeAI('AIzaSyBpsnkJXsgag3yoCQkhZroIApFeGYnJDaw'); // Replace with your actual API key
  }

  async generateText(prompt: string): Promise<void> {
    const model = this.generativeAI.getGenerativeModel({ model: 'gemini-pro' });
    this.messageHistory.next({
      from: 'user',
      message: prompt
    });

    try {
      const result = await model.generateContent(prompt);
      const response = result.response;
      const text = response.text();
      console.log(text);

      this.messageHistory.next({
        from: 'bot',
        message: text
      });
    } catch (error) {
      console.error('Error generating text:', error);
      this.messageHistory.next({
        from: 'error',
        message: 'Error generating text: '
      });
    }
  }

  public getMessageHistory(): Observable<any> {
    return this.messageHistory.asObservable();
  }
}
