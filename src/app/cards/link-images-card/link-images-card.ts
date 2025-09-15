import { Component, signal, WritableSignal } from '@angular/core';
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
  ImageWithLinks: WritableSignal<ImageWithLink[]> = signal([
    {ImageUrl:"background.jpg", link:"https://in.pinterest.com/pin/37436240649728416/", relevance:1},
    {ImageUrl:"background.jpg", link:"https://in.pinterest.com/pin/37436240649728416/", relevance:0},
    {ImageUrl:"background.jpg", link:"https://in.pinterest.com/pin/37436240649728416/", relevance:0},
    {ImageUrl:"background.jpg", link:"https://in.pinterest.com/pin/37436240649728416/", relevance:0},
    {ImageUrl:"background.jpg", link:"https://in.pinterest.com/pin/37436240649728416/", relevance:1}
  ])
}
