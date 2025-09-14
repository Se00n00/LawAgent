import { AfterViewInit, Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

interface summary{
  heading:string
  content:string
}
@Component({
  selector: 'app-summary-card',
  imports: [CommonModule],
  templateUrl: './summary-card.html',
  styleUrl: './summary-card.css'
})
export class SummaryCard implements OnInit, AfterViewInit {
  Summaries:summary[] = [
    {heading:"2025", content:"Explosive growth of delhi which underwent a huge success for the  people of this country"},
    {heading:"2025", content:"Explosive growth of delhi"}
  ]
  setHeight() {
    const sourceDiv = document.getElementById("summaryContent");
    const targetDiv = document.getElementById("Line");
    const summaryItems = document.getElementsByClassName("summaryItem");

    if (sourceDiv && targetDiv && summaryItems.length > 0) {
      const sourceDivHeight = sourceDiv.offsetHeight;
      const lastDiv = summaryItems[summaryItems.length - 1] as HTMLElement;
      
      const lastDivHeight = lastDiv.offsetHeight;
      targetDiv.style.height = (sourceDivHeight - lastDivHeight) + 'px';
    }
}
  ngOnInit(): void {
    this.setHeight()
  }
  ngAfterViewInit(): void {
      this.setHeight()
  }
}
