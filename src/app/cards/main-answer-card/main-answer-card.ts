import { Component, signal, WritableSignal } from '@angular/core';
import { Subject } from 'rxjs';
import { MarkdownComponent} from 'ngx-markdown'
@Component({
  selector: 'app-main-answer-card',
  imports: [MarkdownComponent],
  templateUrl: './main-answer-card.html',
  styleUrl: './main-answer-card.css'
})
export class MainAnswerCard {
  private stream$ = new Subject<string>();
  MainAnswerTitle:WritableSignal<string> = signal("Few Things");
  MainAnswer: WritableSignal<string> = signal("")
  constructor(){
    this.stream$.subscribe(
      chunk => {
        this.MainAnswer.update(prev => prev+chunk)
      }
    )
    // this.queryLLM("Write 100 words about current law system in india, in perfect markdown format")
  }

  async queryLLM(prompt: string) {
    let res = await fetch("https://lawagent-6r30.onrender.com/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: prompt })
    });

    const reader = res.body?.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { done, value } = await reader!.read();
      if (done) break;
      const chunk = decoder.decode(value, { stream: true });
      this.MainAnswer.update(prev => prev + chunk);
    }
  }
}
