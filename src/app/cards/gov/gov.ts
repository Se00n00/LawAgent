import { Component, Input, signal, SimpleChanges } from '@angular/core';
import { CommonModule } from '@angular/common';
interface GovArticles{
  title:string
  url:string
  snippet:string
}

@Component({
  selector: 'app-gov',
  imports: [CommonModule],
  templateUrl: './gov.html',
  styleUrl: './gov.css'
})
export class Gov {
  @Input() Content: GovArticles[] = []
  current_item?: GovArticles
  current_index = signal(0);

  ngOnChanges(changes: SimpleChanges) {
    if (changes['Content'] && Array.isArray(this.Content) && this.Content.length > 0) {
      this.current_index.set(0);
      this.current_item = this.Content[this.current_index()];
    }
  }

  next() {
    const newIndex = (this.current_index() + 1) % this.Content.length;
    this.current_index.set(newIndex);
    this.current_item = this.Content[newIndex];
  }
}
