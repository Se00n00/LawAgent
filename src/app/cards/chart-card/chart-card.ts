import { Component, OnInit } from '@angular/core';
import {Chart} from 'chart.js/auto';
@Component({
  selector: 'app-chart-card',
  imports: [],
  templateUrl: './chart-card.html',
  styleUrl: './chart-card.css'
})
export class ChartCard implements OnInit{
  data:any = {
    labels: [
      'Red',
      'Blue',
      'Yellow'
    ],
    datasets: [{
      label: 'My First Dataset',
      data: [300, 50, 100],
      backgroundColor: [
        'rgb(255, 99, 132)',
        'rgb(54, 162, 235)',
        'rgb(255, 205, 86)'
      ],
      hoverOffset: 4
    }]
  };
  config:any = {
    type: 'doughnut',
    data: this.data,
  };

  public chart:any
  ngOnInit(): void {
    this.chart = new Chart('MyChart', {
      type: 'doughnut', //this denotes tha type of chart
      data: this.data,
      options: {
        aspectRatio: 1,
      },
    });
  }
}
