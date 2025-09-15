import { Component, signal, WritableSignal } from '@angular/core';
import { CommonModule } from '@angular/common';
import {FormsModule} from '@angular/forms';

@Component({
  selector: 'app-questioncard',
  imports: [
    CommonModule,
    FormsModule
  ],
  templateUrl: './questioncard.html',
  styleUrl: './questioncard.css'
})
export class Questioncard {
  askQuestion = signal(true)
  Question: WritableSignal<string> = signal("");


  isTouched: WritableSignal<boolean> = signal(false);
  IsAskQuestionValid(): boolean {
    return this.Question().trim().length === 0;
  }

  running_status_text = "This would take a least time "

  progress = signal(50);
  steps = Array(30).fill(0); // total steps
  get filledSteps() {
    return Math.round((this.progress() / 100) * this.steps.length);
  }

  get progressColor() {
    if (this.progress() < 40) return 'linear-gradient(to right, #f43f5e, #f97316)';
    if (this.progress() < 70) return 'linear-gradient(to right, #f59e0b, #84cc16)';
    return 'linear-gradient(to right, #22c55e, #3b82f6)';
  }

  stepColor(i: number) {
    if (i < this.filledSteps) {
      if (this.progress() < 40) return 'red';
      if (this.progress() < 70) return 'orange';
      return 'green';
    }
    return '#e5e7eb';
  }

  stopAnswering(){
    this.askQuestion.update((val)=>true)
  }

  Ask() {
    this.isTouched.set(true)
    if (!this.IsAskQuestionValid()) {
      console.log('User asked:', this.Question());
      this.askQuestion.update(val=>false)
      // LLM Call
      this.Question.set('')
      this.isTouched.set(false)
    }
  }
}
