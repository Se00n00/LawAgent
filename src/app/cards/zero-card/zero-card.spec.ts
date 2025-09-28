import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ZeroCard } from './zero-card';

describe('ZeroCard', () => {
  let component: ZeroCard;
  let fixture: ComponentFixture<ZeroCard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ZeroCard]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ZeroCard);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
