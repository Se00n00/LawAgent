import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ChartCard } from './chart-card';

describe('ChartCard', () => {
  let component: ChartCard;
  let fixture: ComponentFixture<ChartCard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ChartCard]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ChartCard);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
