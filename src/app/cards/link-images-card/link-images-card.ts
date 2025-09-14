import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
@Component({
  selector: 'app-link-images-card',
  imports: [CommonModule],
  templateUrl: './link-images-card.html',
  styleUrl: './link-images-card.css'
})
export class LinkImagesCard {
  ImageWithLinks = signal([
    {"ImageUrl":"background.jpg", "link":"https://in.pinterest.com/pin/37436240649728416/"},
    {"ImageUrl":"background.jpg", "link":"www.google.com"},
    {"ImageUrl":"background.jpg", "link":"www.google.com"},
    {"ImageUrl":"background.jpg", "link":"www.google.com"},
    {"ImageUrl":"background.jpg", "link":"www.google.com"},
    {"ImageUrl":"background.jpg", "link":"www.google.com"}
  ])
}
