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
  objectKeys(obj: any): string[] {
    return Object.keys(obj);
  }
  Components = signal([
    {"type":"MainAnswer","content":"Hello! everyone **I am Mohit**"}
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
    let braceCount = 0;
    let inString = false;

    while (true) {
      const { done, value } = await reader!.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });

      let start = 0;
      for (let i = 0; i < buffer.length; i++) {
        const char = buffer[i];

        // track strings (ignore braces inside strings)
        if (char === '"' && buffer[i - 1] !== "\\") {
          inString = !inString;
        }

        if (!inString) {
          if (char === "{") braceCount++;
          if (char === "}") braceCount--;

          // full JSON object found
          if (braceCount === 0 && start <= i) {
            const jsonStr = buffer.slice(start, i + 1).trim();
            if (jsonStr) {
              try {
                const dict = JSON.parse(jsonStr);
                this.Components.update(prev => [...prev, dict]);
              } catch (e) {
                console.error("Bad JSON chunk:", jsonStr, e);
              }
            }
            start = i + 1;
          }
        }
      }
      buffer = buffer.slice(start);
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
