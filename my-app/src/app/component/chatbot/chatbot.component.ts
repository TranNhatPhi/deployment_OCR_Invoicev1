import {Component, inject, OnInit} from '@angular/core';
import {FormsModule} from "@angular/forms";
import {DatePipe, NgClass, NgForOf, NgIf} from "@angular/common";
import {ChatgptService} from "../../chatgpt.service";
import {Gemini2Service} from "../../gemini2.service";
import {GeminiService} from "../../gemini.service";
@Component({
  selector: 'app-chatbot',
  standalone: true,
  imports: [
    FormsModule,
    NgClass,
    NgForOf,
    NgIf,
    DatePipe
  ],
  templateUrl: './chatbot.component.html',
  styleUrl: './chatbot.component.scss'
})
export class ChatbotComponent implements OnInit {
  messages: { sender: string, content: string, timestamp: Date }[] = [
    { sender: 'gpt', content: 'Xin chào, tôi có thể giúp gì cho bạn?', timestamp: new Date() }
  ];
  title = 'gemini-inte';

  prompt: string = '';
  loading: boolean = false;
  question: string = '';
  showChat: boolean = true;
  selectedChatbot: string = 'chatgpt'; // Initialize the selected chatbot
  chatHistory: any[] = [];

  constructor(
    private chatService: ChatgptService,
    private gemini2Service: Gemini2Service
  ) { }

  ngOnInit(): void {
   /* this.loadHistory();*/
    this.gemini2Service.getMessageHistory().subscribe((res) => {
      if (res) {
        this.chatHistory.push(res);
        this.messages.push({ sender:'', content: res.messages, timestamp: new Date() });
        this.saveHistory();
      }
    });
    const storedContent = localStorage.getItem('fileContent');
    if (storedContent) {
      console.log('Stored file content loaded.');
    }
  }

  onFileSelected(event: any) {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e: any) => {
        const content = e.target.result;
        localStorage.setItem('fileContent', content);
        console.log('File content saved to localStorage');
      };
      reader.readAsText(file);
    }
  }

  loadHistory() {
    const storedMessages = localStorage.getItem('chatHistory');
    if (storedMessages) {
      this.messages = JSON.parse(storedMessages);
    }
  }

  saveHistory() {
    localStorage.setItem('chatHistory', JSON.stringify(this.messages));
  }

  send() {
    const fileContent = localStorage.getItem('fileContent');
    if (fileContent) {
      this.sendMessage(fileContent);
    } else {
      alert('Please upload a file first.');
    }
  }

  sendMessage(fileContent: string) {
    if (!this.question) {
      alert('Please enter a question.');
      return;
    }

    const content = `File Content: ${fileContent}\n\nQuestion: ${this.question}`;
    const selectedService = this.selectedChatbot === 'chatgpt' ? this.chatService : this.gemini2Service; // Choose the service based on selected chatbot

    this.addChatMessage('user', this.question);

    if (this.selectedChatbot === 'chatgpt') {
      if (!(selectedService instanceof Gemini2Service)) {
        selectedService.sendMessage(content).subscribe({
          next: (response: any) => {
            const sender = 'gpt';
            const messageContent = response.choices[0].message.content;
            this.typeWriter(sender, messageContent);
            console.log(response);
          },
          complete: () => {
            console.log('Message sent successfully');
          },
          error: (error: any) => {
            console.error('Error sending message:', error);
            this.addChatMessage('error', 'Error sending message: ' + error.message);
          }
        });
      }
    } else {
      this.gemini2Service.generateText(content);
    }

    this.question = '';
  }

  addChatMessage(sender: string, message: string) {
    this.messages.push({ sender, content: message, timestamp: new Date() });
    this.saveHistory();
  }

  typeWriter(sender: string, text: string) {
    let i = 0;
    const message = { sender, content: '', timestamp: new Date() };
    this.messages.push(message);
    const interval = setInterval(() => {
      if (i < text.length) {
        message.content += text.charAt(i);
        i++;
      } else {
        clearInterval(interval);
        this.saveHistory();
      }
    }, 30);
  }
}
