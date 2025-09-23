import { Component, Input, signal, WritableSignal } from '@angular/core';
import { CommonModule } from '@angular/common';

interface ImageWithLink{
  ImageUrl:string
  link:string
  relevance:number
}

@Component({
  selector: 'app-link-images-card',
  imports: [CommonModule],
  templateUrl: './link-images-card.html',
  styleUrl: './link-images-card.css'
})


export class LinkImagesCard {
  @Input() ImageWithLinks: ImageWithLink[] = []
}
