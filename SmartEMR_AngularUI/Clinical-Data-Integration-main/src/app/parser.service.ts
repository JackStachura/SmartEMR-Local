import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class ParserService {
  
  url = 'http://localhost:8080';

  getConfig() {
    this.http.post(this.url, {"NLQuery":"Show all from clinical_notes"}, {{"Content-Type":"application/json"}});
    return this.http.get(this.url);
  }

  constructor(private http: HttpClient) { }
}
