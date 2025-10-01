import { Component, Input, WritableSignal, signal, computed } from '@angular/core';
import { single } from 'rxjs';
import { DatePipe } from '@angular/common';
interface Newscard{
  title: string
  body: string
  article_url:string
  image_url: string
  source: string
  date: string
}

@Component({
  selector: 'app-news-cards',
  imports: [DatePipe],
  templateUrl: './news-cards.html',
  styleUrl: './news-cards.css'
})

export class NewsCards {
  

  @Input() NewscardItems: Newscard[] = []
  CurrentCardIndex = signal(0)
  
  NewscardItem = computed(() => {
    const items = this.NewscardItems
    const index = this.CurrentCardIndex()
    return items.length ? items[index] : null
  })

  changeCardIndex(cardIndex: number) {
    if (this.NewscardItems.length) {
      this.CurrentCardIndex.set(cardIndex % this.NewscardItems.length)
    }
  }

  incrementCardIndex(increment: number) {
    if (this.NewscardItems.length) {
      const length = this.NewscardItems.length
      this.CurrentCardIndex.update(val => (val + increment + length) % length)
    }
  }
  next(){
    const newIndex = (this.CurrentCardIndex() + 1) % this.NewscardItems.length;
    this.CurrentCardIndex.set(newIndex);
    this.body.set(false)
  }

  body = signal(false)
  showBody(){
    this.body.update((val)=> val = !val)
  }
}
