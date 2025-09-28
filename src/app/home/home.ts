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
import { ZeroCard } from '../cards/zero-card/zero-card';

interface output{
  type:string
  content:any
}

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
    ChartCard,
    ZeroCard
  ],
  
  templateUrl: './home.html',
  styleUrl: './home.css'
})
export class Home {
  constructor(public auth:Supabase){}
  objectKeys(obj: any): string[] {
    return Object.keys(obj);
  }
  Components:WritableSignal<output[]> = signal([
    {"type":"ZeroCard", "content":""},
  ])
  MasterQuestion: WritableSignal<string> = signal("")
  Answer: WritableSignal<string> = signal("")


  removeIntro = signal(false)
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
    let buffer = "";

    while (true) {
      const { done, value } = await reader!.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });

      // The backend separates JSONs with spaces → split them
      const parts = buffer.split("} {").map((p, i, arr) => {
        if (arr.length === 1) return p;
        if (i < arr.length - 1) return p + "}";
        if (i > 0) return "{" + p;
        return p;
      });

      // Try parsing all complete JSON objects except last (may be partial)
      for (let i = 0; i < parts.length - 1; i++) {
        try {
          const obj = JSON.parse(parts[i]);
          this.Components.update(prev => [...prev, obj]);
        } catch (e) {
          // ignore until JSON is complete
        }
      }

      // Keep last fragment in buffer for next loop
      buffer = parts[parts.length - 1];
    }

    // Parse last leftover if valid
    if (buffer.trim()) {
      try {
        const obj = JSON.parse(buffer);
        this.Components.update(prev => [...prev, obj]);
      } catch (e) {
        console.error("Leftover not valid JSON:", buffer);
      }
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
