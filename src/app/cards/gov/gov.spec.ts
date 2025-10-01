import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Gov } from './gov';

describe('Gov', () => {
  let component: Gov;
  let fixture: ComponentFixture<Gov>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Gov]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Gov);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
