import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AssistedQueryComponent } from './assisted-query.component';

describe('AssistedQueryComponent', () => {
  let component: AssistedQueryComponent;
  let fixture: ComponentFixture<AssistedQueryComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AssistedQueryComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AssistedQueryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
