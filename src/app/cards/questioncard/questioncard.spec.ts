import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Questioncard } from './questioncard';

describe('Questioncard', () => {
  let component: Questioncard;
  let fixture: ComponentFixture<Questioncard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Questioncard]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Questioncard);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
