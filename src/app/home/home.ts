import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { Questioncard } from '../cards/questioncard/questioncard';
import { NewsCards } from '../cards/news-cards/news-cards';
import { SummaryCard } from '../cards/summary-card/summary-card';
import { MainAnswerCard } from '../cards/main-answer-card/main-answer-card';
import { ErrorCard } from '../cards/error-card/error-card';
import { LinkImagesCard } from '../cards/link-images-card/link-images-card';
import { ChartCard } from '../cards/chart-card/chart-card';

@Component({
  selector: 'app-home',
  imports: [
    CommonModule, 
    RouterLink, 
    Questioncard, 
    NewsCards,
    SummaryCard,
    MainAnswerCard,
    ErrorCard,
    LinkImagesCard,
    ChartCard
  ],
  
  templateUrl: './home.html',
  styleUrl: './home.css'
})
export class Home {
  placeholder="Discuss about new case !"
  removeIntro = signal(false)
  askNext = signal(false)

  Searching = signal(false)

  SearchIcon="Icons/add.svg"

  showMainSearchInput(){
    this.Searching.update((val)=>val = !val)
  }
}
