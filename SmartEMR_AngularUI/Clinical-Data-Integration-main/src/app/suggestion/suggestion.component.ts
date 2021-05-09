import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { Tag } from '../tag';

@Component({
  selector: 'app-suggestion',
  templateUrl: 'suggestion.component.html',
  styleUrls: ['suggestion.component.scss']
})
export class SuggestionComponent implements OnInit {
  @Input() suggestion: Tag;
  @Output() closed = new EventEmitter<Tag>();

  constructor() { }

  ngOnInit() { }

  onSuggestionClicked(suggestion: Tag) {
    this.closed.emit(suggestion);
  }
}