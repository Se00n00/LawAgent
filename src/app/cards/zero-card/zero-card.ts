import { Component, EventEmitter, Output } from '@angular/core';
import { RouterLink } from '@angular/router';
import { Router } from '@angular/router';

@Component({
  selector: 'app-zero-card',
  imports: [RouterLink],
  templateUrl: './zero-card.html',
  styleUrl: './zero-card.css'
})
export class ZeroCard {
  constructor(private router: Router) {}
  @Output() messageEvent = new EventEmitter<boolean>();

  newConversation(){
    this.messageEvent.emit(true)
  }
}
