import { Component, Input, signal, WritableSignal } from '@angular/core';
import { CommonModule } from '@angular/common';

interface ImageWithLink{
  image_url:string
  title:string
  article_url:string
}

@Component({
  selector: 'app-link-images-card',
  imports: [CommonModule],
  templateUrl: './link-images-card.html',
  styleUrl: './link-images-card.css'
})


export class LinkImagesCard {
  @Input() ImageWithLinks: ImageWithLink[] = [
    {'image_url':'images/0Node.png','article_url':'','title':'title'}
  ]
}
