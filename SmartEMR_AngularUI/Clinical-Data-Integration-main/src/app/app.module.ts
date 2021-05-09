import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NavListComponent } from './nav-list/nav-list.component';
import { LoginComponent } from './login/login.component';
import { SqlQueryComponent } from './sql-query/sql-query.component';
import { AssistedQueryComponent } from './assisted-query/assisted-query.component';
import { AboutComponent } from './about/about.component';
import { ContactComponent } from './contact/contact.component';
import { HomeComponent } from './home/home.component';
import { UploadDataComponent } from './upload-data/upload-data.component';
import { TagComponent } from './tag/tag.component';
import { TagsComponent } from './tags/tags.component';
import { SuggestionComponent } from './suggestion/suggestion.component';
import { TagService } from "./tag.service";
import { TagFilterPipe } from "./tag-filter.pipe";
import { BrowserAnimationsModule } from "@angular/platform-browser/animations";
import { PatientProfileComponent } from './patient-profile/patient-profile.component';


@NgModule({
  declarations: [
    AppComponent,
    NavListComponent,
    LoginComponent,
    SqlQueryComponent,
    AssistedQueryComponent,
    AboutComponent,
    ContactComponent,
    HomeComponent,
    UploadDataComponent,
    TagComponent,
    TagsComponent,
    TagFilterPipe,
    SuggestionComponent,
    PatientProfileComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    BrowserAnimationsModule
  ],
  providers: [TagService, NavListComponent],
  bootstrap: [
    AppComponent,
    LoginComponent
  ]
})
export class AppModule { }
