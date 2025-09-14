import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MainAnswerCard } from './main-answer-card';

describe('MainAnswerCard', () => {
  let component: MainAnswerCard;
  let fixture: ComponentFixture<MainAnswerCard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MainAnswerCard]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MainAnswerCard);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
