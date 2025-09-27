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
  

  @Input() NewscardItems: Newscard[] = [
    // {
    //   article_id:1,
    //   article_author:"sfd",
    //   article_author_icon:"sd",
    //   article_head:"df",
    //   article_head_image_url:"df",
    //   article_origin_web_url:"df",
    //   article_orign_web_icon:"as",
    //   article_summerized_content:"sd"
    // }
  ]
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
