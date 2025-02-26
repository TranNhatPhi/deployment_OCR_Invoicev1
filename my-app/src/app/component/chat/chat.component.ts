import {Component, OnInit} from '@angular/core';
import { ChatgptService } from '../../chatgpt.service';
import { SharedModule } from '../../shared-module';


@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [SharedModule],
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.scss']
})
  export class ChatComponent implements OnInit{
  messages: { sender: string, content: string,timestamp:Date }[] = [
    { sender: 'gpt', content: 'Xin chào, tôi có thể giúp gì cho bạn?',timestamp: new Date() }
  ];
  question: string = '';
  showChat: boolean = true;

  constructor(private chatService: ChatgptService) { }


  ngOnInit(): void {
    /*this.loadHistory();*/
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
        localStorage.setItem('fileContent', content);  // Save file content to local storage
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

    this.addChatMessage('user', this.question);

    this.chatService.sendMessage(content).subscribe({
      next: (response: any) => {
        this.typeWriter('gpt', response.choices[0].message.content);
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

    this.question = '';
  }


  addChatMessage(sender: string, message: string) {
    this.messages.push({ sender, content: message,timestamp:new Date() });
    this.saveHistory();
  }

  typeWriter(sender: string, text: string) {
    let i = 0;
    const message = { sender, content: '',timestamp:new Date()};
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
