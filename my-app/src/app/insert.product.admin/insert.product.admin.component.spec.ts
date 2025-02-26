import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InsertProductAdminComponent } from './insert.product.admin.component';

describe('InsertProductAdminComponent', () => {
  let component: InsertProductAdminComponent;
  let fixture: ComponentFixture<InsertProductAdminComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [InsertProductAdminComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(InsertProductAdminComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
