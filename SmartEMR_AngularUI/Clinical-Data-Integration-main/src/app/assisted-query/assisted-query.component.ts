import { Component, OnInit, OnDestroy, Renderer2, ViewChild, ElementRef } from '@angular/core';
import { FormBuilder, FormControl, FormGroup } from "@angular/forms";
import { HttpClient, HttpHeaders } from "@angular/common/http";
import embed from "vega-embed";
import { DataService } from '../shared/data.service';
import { takeUntil } from 'rxjs/operators';
import { Subject } from 'rxjs';
//import { DataTableDirective } from 'angular-datatables';
//import * as myGlobals from '../../globals';

@Component({
  selector: 'app-assisted-query',
  templateUrl: './assisted-query.component.html',
  styleUrls: ['./assisted-query.component.css']
})
export class AssistedQueryComponent implements OnInit {

  formGroup: FormGroup;
  formGroup2: FormGroup;
  destroy$: Subject<boolean> = new Subject<boolean>();

  activate: boolean = false;
  visualization: boolean = false;
  images: string[] = [];

  queries: string[] = [];
  latestQuery: string;

  getimageurl: string = "http://sdpimageapi.azurewebsites.net/file/";
  httpClient: any;
  response_table: string[] = this.dataService.response_table;
  vis_activate: boolean = false;
  sql_statement: string = "";

  //dtOptions: DataTables.Settings = {};

  showVisBox: boolean = false;

  createChart() {
    this.dataService.getGraphData().pipe(takeUntil(this.destroy$)).subscribe(
      (data: any) => {
        console.log(data)
      }
    );
  }

  findImages(formData: { [x: string]: any }) {    
    this.dataService.getNLImageQuery(formData["query"]).pipe(takeUntil(this.destroy$)).subscribe(
      (data: any) => {
        this.images = [];
        console.log(data)
        for (var i = 0; i < data.length; i++) {
          this.images.push(data[i])
        }
      }
    );
  }

  update(formData: { [x: string]: any }) {
    this.queries.push(formData["query"]);
    this.latestQuery = formData["query"];
  }

  onSubmit(formData: { [x: string]: any }) {
    this.http
      .get("http://localhost:5000/graph", {
        params: {
          query: formData["query"]
        }
      })
      .subscribe(data => {
        let spec = data[0];
        console.log(spec);
        embed("#vis", spec, { actions: false });
      });
  }
  onSubmitAssisted(formData: { [x: string]: any }) {
    this.update2(formData["query"]);
    this.dataService.sendAssisted(formData["query"]).pipe(takeUntil(this.destroy$)).subscribe(
      (data: any) => {
        console.log(data['Data'])
        if (data['Data'] == 'NONE') {
          this.response_table[0] = "NONE";
        }
        else {
          this.response_table = data['Data'];
          this.sql_statement = data['SQL'];
          for (let i = 0; i < this.response_table.length; i++) {
            var str: string = this.response_table[i];
            this.response_table[i] = (str).toString().replace(/,/g, " ")
          }
          console.log(this.response_table[0]);
          console.log(this.response_table.length);
          console.log(this.activate);
         
        }
      }
    );
  }
  onSubmitAnalysis(formData2: { [x: string]: any }) {
    //"http://sdp2.cse.uconn.edu:5000/graph\?query\=show%20me%20a%20chart%20of%20different%20drugs\&sql\=SELECT%20\*%20FROM%20clinical_notes\;";
    let url = "http://sdp2.cse.uconn.edu:5000/graph\?query\=QUERY\&sql\=SQL\;";
    let url2 = url.replace(/QUERY/g, formData2.query2.trim().replace(/ /g, "%20"));
    let url3 = url2.replace(/SQL/g, this.sql_statement.trim().replace(/ /g, "%20").replace(/;/g, ""));

    this.showVisBox = true;

    console.log(url3);
    this.http
      .get(url3)
      .subscribe(data => {
        let spec = data[0];
        if (spec != []) {
          embed("#vis", spec, { actions: false });
        }
      });
  }  
  

  update2(query: string) {
    this.queries.push(query);
    this.latestQuery = query;
  }

  pinSearch(formData: { [x: string]: any }){
    let stringToSave = formData["query"];
    this.dataService.assisted_query_pre = stringToSave;
    console.log(this.dataService.assisted_query_pre);
    this.dataService.response_table = this.response_table;
    
  }

  findImages2(query: string) {
    
    this.dataService.getNLImageQuery(query).pipe(takeUntil(this.destroy$)).subscribe(
      (data: any) => {
        this.images = [];
        console.log(data)
        for(var i = 0; i < data.length; i++) {
          this.images.push(data[i])
        }
      }
    );
  }

  onSubmit2(query: string) {
    this.dataService.sendAssisted(query).pipe(takeUntil(this.destroy$)).subscribe(
      (data: any) => {
        console.log(data['Data'])
        if (data['Data'] == 'NONE') {
          this.response_table[0] = "NONE";
        }
        else {
          this.response_table = data['Data'];
          this.sql_statement = data['SQL'];
          for (let i = 0; i < this.response_table.length; i++) {
            var str: string = this.response_table[i];
            this.response_table[i] = (str).toString().replace(/,/g, " ")
          }
          console.log(this.response_table[0]);
          console.log(this.response_table.length);
          console.log(this.activate);
         
        }
      }
    );
  }


  constructor(private http: HttpClient, private formBuilder: FormBuilder, private dataService: DataService, private renderer: Renderer2, private e: ElementRef) {
    this.formGroup = this.formBuilder.group({
      query: ""
    });
    this.formGroup2 = this.formBuilder.group({
      query2: new FormControl("")
    });
  }

  ngOnInit() {
//    this.dtOptions = {
//      columnDefs: [
//        {
//          targets: [10],
//          "orderable": false,
//        },
//      ],
//      pagingType: 'full_numbers',
//      pageLength: 3,
//    };
    if(this.dataService.response_table.length != 0){
      this.activate = true;
      this.response_table = this.dataService.response_table;
    }
    
  }

  ngOnDestroy() {
    this.destroy$.next(true);
    this.destroy$.unsubscribe();
  }
}