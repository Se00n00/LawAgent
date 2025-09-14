import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { Questioncard } from '../cards/questioncard/questioncard';
import { NewsCards } from '../cards/news-cards/news-cards';
import { SummaryCard } from '../cards/summary-card/summary-card';
@Component({
  selector: 'app-home',
  imports: [
    CommonModule, 
    RouterLink, 
    Questioncard, 
    NewsCards,
    SummaryCard
  ],
  
  templateUrl: './home.html',
  styleUrl: './home.css'
})
export class Home {
  placeholder="What you want to ask?"
  removeIntro = signal(false)
  askNext = signal(false)
}
