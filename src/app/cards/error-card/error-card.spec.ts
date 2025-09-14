import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ErrorCard } from './error-card';

describe('ErrorCard', () => {
  let component: ErrorCard;
  let fixture: ComponentFixture<ErrorCard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ErrorCard]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ErrorCard);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
