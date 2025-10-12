import { AfterViewInit, Component, ElementRef, Input, input, OnInit, signal, ViewChild, WritableSignal } from '@angular/core';
import { CommonModule } from '@angular/common';

interface summary{
  heading:string
  heading_content:string
}
@Component({
  selector: 'app-summary-card',
  imports: [CommonModule],
  templateUrl: './summary-card.html',
  styleUrl: './summary-card.css'
})
export class SummaryCard implements OnInit, AfterViewInit {

  // Input Data to Summary Card
  @Input() SummaryTitle: string = "";
  @Input() Summaries: summary[] = [];

  @ViewChild('SummaryElement') summary: ElementRef|any;
  

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

  direction: 'down' | 'up' = 'down';

  scroll_next() {
    const element = this.summary.nativeElement;
    const maxScroll = element.scrollHeight - element.clientHeight;

    if (this.direction === 'down') {
      element.scroll({
        top: element.scrollTop + 100,
        behavior: 'smooth'
      });
      if (element.scrollTop + element.clientHeight >= element.scrollHeight) {
        this.direction = 'up';
      }
    } else {
      element.scroll({
        top: 0,
        behavior: 'smooth'
      });
      if (element.scrollTop <= 0) {
        this.direction = 'down';
      }
    }
  }

}
