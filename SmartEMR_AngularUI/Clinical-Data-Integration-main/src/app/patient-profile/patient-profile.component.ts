import { DOCUMENT } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { collectExternalReferences } from '@angular/compiler';
import { Component, Inject, OnInit } from '@angular/core';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { DataService } from '../shared/data.service';
@Component({
  selector: 'app-patient-profile',
  templateUrl: './patient-profile.component.html',
  styleUrls: ['./patient-profile.component.css']
})
export class PatientProfileComponent implements OnInit {

  constructor(@Inject(DOCUMENT) private document : Document, private dataService : DataService) { }
  creationShown : boolean;
  destroy$: Subject<boolean> = new Subject<boolean>();
  ngOnInit(): void {
    
  }
  showOrHidePatientCreation() : void {
    var button = document.getElementById('creation-button');
    button.classList.toggle('active');
    button.innerHTML = "Create Patient Profile"
    var content = document.getElementById('create-form');
   
     if (content.style.maxHeight){
          content.style.maxHeight = null;
         
        } else {
          button.textContent = "Collapse";
          content.style.maxHeight = content.scrollHeight + "px";
          
        }
  }
  showOrHidePatientFetch() {
     var button = document.getElementById('fetch-button');
     button.innerHTML = "Search Patient Profile"
    var content = document.getElementById('fetch-form');
    
     if (content.style.maxHeight){
          content.style.maxHeight = null;
        } else {
          button.innerHTML = "Collapse";
          content.style.maxHeight = content.scrollHeight + "px";
         
        }
      }
  searchForm(): void {
    //function to prepare and send creation form to OpenEMR
    //get elements from creation form
    var creation_params = document.getElementsByClassName('form-controlS');
    for(let i = 0; i < creation_params.length; i++){
      var fname = (creation_params[0] as HTMLInputElement).value;
      var lname = (creation_params[1] as HTMLInputElement).value;
      var pid = (creation_params[2] as HTMLInputElement).value;
      var city = (creation_params[3] as HTMLInputElement).value;
      var state = (creation_params[4] as HTMLInputElement).value;
      var zip = (creation_params[5] as HTMLInputElement).value;
      
    }
    
  }
  createForm(): void {
    //function to prepare and send a search request. Displays a card of the patient profile.
    var creation_params = document.getElementsByClassName('form-controlC');
    
    var fname = (creation_params[0] as HTMLInputElement).value;
    var lname = (creation_params[1] as HTMLInputElement).value;
    var pid = (creation_params[2] as HTMLInputElement).value;
    var DOB = (creation_params[3] as HTMLInputElement).value;
    var phone = (creation_params[4] as HTMLInputElement).value;
    var ssn4 = (creation_params[5] as HTMLInputElement).value;
    
    this.dataService.sendPatientCreation(fname, lname, pid, DOB, phone, ssn4).pipe(takeUntil(this.destroy$)).subscribe(
      (data: any) => {
        console.log(data)

        }
      
    );
    }
    ngOnDestroy() {
      this.destroy$.next(true);
      this.destroy$.unsubscribe();
    }
  }

