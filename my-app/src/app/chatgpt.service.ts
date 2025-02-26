import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ChatgptService {
  private apiUrl = '';
  private apiKey = '';  // Replace with your API key

  constructor(private http: HttpClient) { }

  sendMessage(content: string): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${this.apiKey}`,
      'Content-Type': 'application/json'
    });

    const data = {
      model: 'gpt-3.5-turbo',
      messages: [{
        role: 'user',
        content: content
      }],
      max_tokens: 300
    };

    return this.http.post<any>(this.apiUrl, data, { headers });
  }

}
