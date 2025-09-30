import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ModelErrorCard } from './model-error-card';

describe('ModelErrorCard', () => {
  let component: ModelErrorCard;
  let fixture: ComponentFixture<ModelErrorCard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ModelErrorCard]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ModelErrorCard);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
