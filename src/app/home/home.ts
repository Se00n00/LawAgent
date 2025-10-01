import { Component, signal, WritableSignal, effect, OnInit } from '@angular/core';
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
import { ModelErrorCard } from '../cards/model-error-card/model-error-card';
// import oboe from 'oboe';
import JSONic from 'jsonic';
// @ts-ignore
// import oboe from 'oboe';

declare const clarinet: any;
// // @ts-ignore
// import clarinet from 'clarinet';
// @ts-ignore
declare module 'oboe' {
  const oboe: any;
  export default oboe;
}

// In your component/service
// @ts-ignore
import oboe from 'oboe';

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
    ZeroCard,
    ModelErrorCard
  ],
  
  templateUrl: './home.html',
  styleUrl: './home.css'
})

export class Home{
  constructor(public auth:Supabase){}
  // home.component.ts or wherever you use it
  // clarinet: any;

  objectKeys(obj: any): string[] {
    return Object.keys(obj);
  }
  Components:WritableSignal<output[]> = signal([
    {"type":"ZeroCard", "content":""},
  ])
  progress = 0

  MasterQuestion: WritableSignal<string> = signal("")
  Answer: WritableSignal<string> = signal("")


  removeIntro = signal(true)
  askNext = signal(false)

  Searching = signal(false)

  SearchIcon="Icons/add.svg"
  
  // async queryLLM(prompt: string) {
    

  async queryLLM(prompt: string) {
  const res = await fetch('https://lawagent-6r30.onrender.com/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: prompt })
  });

  const reader = res.body?.getReader();
  const decoder = new TextDecoder();
  let buffer = '';

  while (true) {
    const { done, value } = await reader!.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split('\n');
    buffer = lines.pop()!; // keep last incomplete line

    for (const line of lines) {
      try {
        const obj = JSON.parse(line);
        this.Components.update(prev => [...prev, obj]);
        if (obj.type === 'Status') this.progress = obj.content;
      } catch {
        // not JSON → treat as plain message
        this.Components.update(prev => [...prev, { type: 'message', content: line }]);
      }
    }
  }

  // parse leftover
  if (buffer.trim()) {
    try {
      const obj = JSON.parse(buffer);
      this.Components.update(prev => [...prev, obj]);
      if (obj.type === 'Status') this.progress = obj.content;
    } catch {
      this.Components.update(prev => [...prev, { type: 'message', content: buffer }]);
    }
  }
// }

      
  //   let buffer = '';

  //   while (true) {
  //     const { done, value } = await reader!.read();
  //     if (done) break;

  //     buffer += decoder.decode(value, { stream: true });

  //     let startIdx = buffer.indexOf('{');
  //     while (startIdx !== -1) {
  //       let endIdx = buffer.indexOf('}', startIdx);
  //       if (endIdx === -1) break; // incomplete JSON

  //       const rawObj = buffer.slice(startIdx, endIdx + 1);

  //       try {
  //         const obj = JSONic(rawObj); // tolerant parser
  //         this.Components.update(prev => [...prev, obj]);

  //         if (obj.type === 'Status') {
  //           this.progress = obj.content; // update progress
  //         }

  //         buffer = buffer.slice(endIdx + 1);
  //         startIdx = buffer.indexOf('{');
  //       } catch (e) {
  //         // Could not parse → skip one character and retry
  //         startIdx += 1;
  //       }
  //     }
  //   }

  // // Parse any leftover
  //   if (buffer.trim()) {
  //     try {
  //       const obj = JSONic(buffer);
  //       this.Components.update(prev => [...prev, obj]);
  //       if (obj.type === 'Status') this.progress = obj.content;
  //     } catch (e) {
  //       console.error('Leftover not valid JSON:', buffer);
  //     }
  //   }
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
