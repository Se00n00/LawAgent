import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NewsCards } from './news-cards';

describe('NewsCards', () => {
  let component: NewsCards;
  let fixture: ComponentFixture<NewsCards>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [NewsCards]
    })
    .compileComponents();

    fixture = TestBed.createComponent(NewsCards);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
