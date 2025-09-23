import { Component, Input, WritableSignal, signal, computed } from '@angular/core';
import { single } from 'rxjs';

interface Newscard{
  article_id: number
  article_head: string
  article_head_image_url: string
  article_summerized_content: string
  article_origin_web_url: string
  article_orign_web_icon: string
  article_author: null|string
  article_author_icon:null|string
}

@Component({
  selector: 'app-news-cards',
  imports: [],
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
}
