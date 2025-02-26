import { Component } from '@angular/core';
import { FooterComponent } from '../footer/footer.component';
import { HeaderComponent } from '../header/header.component';
import { ChatComponent } from '../chat/chat.component';


@Component({
    selector: 'app-contact',
    standalone: true,
    imports: [HeaderComponent, FooterComponent, ChatComponent],
    templateUrl: './contact.component.html',
    styleUrl: './contact.component.scss'
})
export class ContactComponent {
}
