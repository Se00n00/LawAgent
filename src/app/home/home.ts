import { Component, signal, WritableSignal, effect } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { Questioncard } from '../cards/questioncard/questioncard';
import { NewsCards } from '../cards/news-cards/news-cards';
import { SummaryCard } from '../cards/summary-card/summary-card';
import { MainAnswerCard } from '../cards/main-answer-card/main-answer-card';
import { ErrorCard } from '../cards/error-card/error-card';
import { LinkImagesCard } from '../cards/link-images-card/link-images-card';
import { ChartCard } from '../cards/chart-card/chart-card';
import { FormsModule } from '@angular/forms';
import { Supabase } from '../service/supabase';

@Component({
  selector: 'app-home',
  imports: [
    CommonModule,
    FormsModule,
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
  constructor(public auth:Supabase){}
  Components = signal([
    {"type":"MainAnswer","content":"Nic"}
  ])
  MasterQuestion: WritableSignal<string> = signal("")
  Answer: WritableSignal<string> = signal("")


  removeIntro = signal(true)
  askNext = signal(false)

  Searching = signal(false)

  SearchIcon="Icons/add.svg"

  async queryLLM(prompt: string) {
    let res = await fetch("https://lawagent-6r30.onrender.com/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: prompt })
    });

    const reader = res.body?.getReader();
    const decoder = new TextDecoder();
    this.Components.update(prev => [
      ...prev, { type: 'MainAnswer', content: '' }
    ]);
    while (true) {
      const { done, value } = await reader!.read();
      if (done) break;
      const chunk = decoder.decode(value, { stream: true });
      
      this.Components.update(prev => {
        const last = prev[prev.length - 1];
        if (last?.type === 'MainAnswer') {
          last.content += chunk;
          return [...prev.slice(0, -1), last];
        }
        return [...prev, { type: 'MainAnswer', content: chunk }];
      });
    }
  }

  showMainSearchInput(){
    
    if(this.MasterQuestion().length > 0){
        

      // LLM Call
      this.queryLLM(this.MasterQuestion())
      

      this.MasterQuestion.set("")
    }
    this.removeIntro.update((val)=>val = !val)
  }
  receiveMessage(msg: string){
    console.log(msg)
    this.queryLLM(msg)
  }


  // Card: Description + Parameters
  // Main Answer Card : Markdown
  // Card Showing + Map ??? : All Screen Setting
  // Converstation History
}
