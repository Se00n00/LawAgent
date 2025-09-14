import { Component, signal } from '@angular/core';

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
  

  card_content = "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Et laudantium, impedit illum, excepturi hic aut possimus esse sapiente quas inventore itaque eligendi magni repellendus rem aperiam atque fugiat quod ducimus."
  NewscardItems: Newscard[] = [
    {article_id:1,
      article_head:this.card_content,
      article_head_image_url:"images/nothing.jpg",
      article_summerized_content:this.card_content,
      article_origin_web_url:"www.google.com",
      article_orign_web_icon:"www.google.com",
      article_author: null,
      article_author_icon: null
    },
    {article_id:2,
      article_head:this.card_content,
      article_head_image_url:"images/nothing.jpg",
      article_summerized_content:this.card_content,
      article_origin_web_url:"www.google.com",
      article_orign_web_icon:"www.google.com",
      article_author:"Arthur wu rote",
      article_author_icon:"as"
    },
    {article_id:3,
      article_head:this.card_content,
      article_head_image_url:"images/nothing.jpg",
      article_summerized_content:"sfdsfd",
      article_origin_web_url:"www.google.com",
      article_orign_web_icon:"Icons/logo.svg",
      article_author:"Arthur wu rote",
      article_author_icon:"as"
    }
  ]
  CurrentCardIndex = signal(0)
  NewscardItem: Newscard
  
  constructor(){
    this.NewscardItem = this.NewscardItems[this.CurrentCardIndex()]
  }
  
  changeCardIndex(cardIndex:number){
    this.CurrentCardIndex.update((val)=>(cardIndex)%this.NewscardItems.length)
    this.NewscardItem = this.NewscardItems[this.CurrentCardIndex()]
  }

}
