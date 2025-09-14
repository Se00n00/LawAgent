import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-questioncard',
  imports: [CommonModule],
  templateUrl: './questioncard.html',
  styleUrl: './questioncard.css'
})
export class Questioncard {
  askQuestion = signal(false)

  running_status_text = "This would take a least time "

  progress = 50; // percentage
  steps = Array(30).fill(0); // total steps
  get filledSteps() {
    return Math.round((this.progress / 100) * this.steps.length);
  }

  get progressColor() {
    if (this.progress < 40) return 'linear-gradient(to right, #f43f5e, #f97316)';
    if (this.progress < 70) return 'linear-gradient(to right, #f59e0b, #84cc16)';
    return 'linear-gradient(to right, #22c55e, #3b82f6)';
  }

  stepColor(i: number) {
    // Gradient coloring based on index
    if (i < this.filledSteps) {
      if (this.progress < 40) return 'red';
      if (this.progress < 70) return 'orange';
      return 'green';
    }
    return '#e5e7eb'; // gray for unfilled
  }

  stopAnswering(){
    this.askQuestion.update((val)=>true)
  }
}
