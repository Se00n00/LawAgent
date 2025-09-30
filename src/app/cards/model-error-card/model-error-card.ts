import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-model-error-card',
  imports: [],
  templateUrl: './model-error-card.html',
  styleUrl: './model-error-card.css'
})
export class ModelErrorCard {
  @Input() e = ""
}
