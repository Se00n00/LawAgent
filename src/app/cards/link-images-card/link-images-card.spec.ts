import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LinkImagesCard } from './link-images-card';

describe('LinkImagesCard', () => {
  let component: LinkImagesCard;
  let fixture: ComponentFixture<LinkImagesCard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LinkImagesCard]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LinkImagesCard);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
