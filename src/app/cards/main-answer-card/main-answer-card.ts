import { Component, signal, WritableSignal } from '@angular/core';
import { Subject } from 'rxjs';

@Component({
  selector: 'app-main-answer-card',
  imports: [],
  templateUrl: './main-answer-card.html',
  styleUrl: './main-answer-card.css'
})
export class MainAnswerCard {
  private stream$ = new Subject<string>();
  MainAnswerTitle:WritableSignal<string> = signal("Ask More about It");

  constructor(){
    this.stream$.subscribe(
      chunk => {
        this.MainAnswerTitle.update(prev => prev+chunk)
      }
    )
    this.queryLLM("Hello")
  }

  async queryLLM(prompt: string) {
    let res = await fetch("https://lawagent-6r30.onrender.com/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt: "Hello" })
    });

    const reader = res.body?.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { done, value } = await reader!.read();
      if (done) break;
      this.stream$.next(decoder.decode(value, { stream: true }));
    }
  }
}
