import { Component, computed, effect,SimpleChanges, EventEmitter, Input, Output, signal, WritableSignal } from '@angular/core';
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
  @Output() messageEvent = new EventEmitter<string>();
  askQuestion = signal(true)

  Question: WritableSignal<string> = signal("");

  isTouched: WritableSignal<boolean> = signal(false);
  IsAskQuestionValid(): boolean {
    return this.Question().trim().length === 0;
  }

  running_status_text = "This would take a least time "

  @Input() progress:any = 0;
  ngOnChanges(changes: SimpleChanges) {
  if (changes['progress']) {
    const newValue = changes['progress'].currentValue;
    if(newValue == 100){
      this.progress = 0
      this.askQuestion.set(true)
    }

  }
}

  
  steps = Array(30).fill(0);

  get filledSteps() {
    return Math.round((this.progress) / 100 * this.steps.length);
  }

  get progressColor() {
    const val = this.progress;
    if (val < 40) return 'linear-gradient(to right, #f43f5e, #f97316)';
    if (val < 70) return 'linear-gradient(to right, #f59e0b, #84cc16)';
    return 'linear-gradient(to right, #22c55e, #3b82f6)';
  }

  stepColor(i: number) {
    const val = this.progress
    if (i < this.filledSteps) {
      if (val < 40) return 'red';
      if (val < 70) return 'orange';
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
      this.messageEvent.emit(this.Question());
      this.Question.set('')
      this.isTouched.set(false)
    }
  }
}
