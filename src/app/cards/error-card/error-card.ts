import { Component, signal, WritableSignal } from '@angular/core';

@Component({
  selector: 'app-error-card',
  imports: [],
  templateUrl: './error-card.html',
  styleUrl: './error-card.css'
})
export class ErrorCard {
  /*
  Error Index:
    0: Mild Dead Ends (Low Severity) - User goes slightly off-topic or asks casual/unrelated stuff <Redirection>
    1: Moderate Dead Ends (Medium Severity) - User tries to derail the flow with something completely unrelated <Redirection>
    2: Strict Dead Ends (High Severity) - User asks for unsafe, harmful, or inappropriate content. <Block>
    3: Extreme Dead Ends (Very High Severity) - User brings up dangerous or crisis-related content (e.g., self-harm, violence) <Block>
  */
  ErrorIndex:WritableSignal<number> = signal(0)
  ErrorList = [
    {"path":"images/DeadEnd/NothingFound.jpg","text":"Seems likes, I have found nothing", "redirection":true, "followUpQuestion":"What could be the reason for such ?"}
  ]
  followUp(followQuestion:string){}
}
