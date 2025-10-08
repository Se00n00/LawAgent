import { Component, EventEmitter, Input, Output, signal, WritableSignal } from '@angular/core';
import { CommonModule } from '@angular/common';
@Component({
  selector: 'app-error-card',
  imports: [CommonModule],
  templateUrl: './error-card.html',
  styleUrl: './error-card.css'
})
export class ErrorCard {
  /*
  Error Index:
    0: Normal flow
    1: Mild Dead Ends (Low Severity) - User goes slightly off-topic or asks casual/unrelated stuff <Redirection>
    2: Moderate Dead Ends (Medium Severity) - User tries to derail the flow with something completely unrelated <Redirection>
    3: Strict Dead Ends (High Severity) - User asks for unsafe, harmful, or inappropriate content. <Block>
    4: Extreme Dead Ends (Very High Severity) - User brings up dangerous or crisis-related content (e.g., self-harm, violence) <Block>
  */
  @Input() Redirection: string|null = null
  @Input() ErrorIndex:number|null = null
  @Output() message = new EventEmitter<string>();

  ErrorList = [
    {"path":"images/DeadEnd/NothingFound.jpg","text":"Seems likes, I have found nothing"},
    {"path":"images/DeadEnd/NewIrrelevent.png","text":"Seems likes, You have lost"},
    {"path":"images/DeadEnd/IrreleventContext.jpg","text":"Woah! your are going too much irrelvent to the context"},
    {"path":"images/DeadEnd/Inappropriate.jpg","text":"DeadEnd: Inappropriate Query"},
    {"path":"images/DeadEnd/Dangerous.jpg","text":"DeadEnd: Dangerous Query! Please seek help"}
  ]
  followUp(followQuestion:string){
    this.message.emit(followQuestion)
  }
}