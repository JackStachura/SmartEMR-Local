import { Component, OnInit } from '@angular/core';
import { DataService } from '../shared/data.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  constructor(private dataService: DataService) { }

  ngOnInit(): void {
  }

  activate: boolean = false;
  validEmails: string[] = ["eric.hilhorst@uconn.edu"];
  validPasswords: string[] = ["test"];
  permission: boolean = false;

  

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

}