import { Component, OnInit } from '@angular/core';
import { DataService } from '../shared/data.service';

@Component({
  selector: 'app-nav-list',
  templateUrl: './nav-list.component.html',
  styleUrls: ['./nav-list.component.css']
})
export class NavListComponent implements OnInit {

  validEmails: string[] = ["eric.hilhorst@uconn.edu"];
  validPasswords: string[] = ["test"];
  validCodes: string[] = ["14"];
  permission: boolean = false;
  activate: boolean = false;
  login: boolean = false;

  constructor(private dataService: DataService) { }

  public updatePermission() {
    this.login = true;
    console.log("THIS GOT CALLED")
  }

  validate(email: string, password: string) {
    console.log(this.validEmails.includes(email))
    console.log(this.validPasswords.includes(password))
    if(this.validEmails.includes(email) && this.validPasswords.includes(password)) {
      this.permission = true;
      this.activate = false;
      //this.navList.updatePermission();
      console.log(this.permission);
    }
    else {
      this.activate = true;
    }
  }

  signUp(email: string, password: string, code: string) {
    if(this.validCodes.includes(code)) {
      this.permission = true;
      this.activate = false;
      
    }
    else {
      this.activate = true;
    }
  }

  ngOnInit(): void {
  }

}
