import { Injectable } from '@angular/core';
import * as matcher from './matcher';
import { Tag } from './tag';

@Injectable()
export class TagService {

  filterSuggestions(suggestions: Tag[], tags: Tag[],  filter: string): Tag[] {
    const distinct = this.outersect(suggestions, tags, (t: Tag) => t.name);
    if (distinct && filter) {
      let searchTerm = filter || '*';
      searchTerm = searchTerm.endsWith('*') ? searchTerm : searchTerm + '*';
      searchTerm = searchTerm.startsWith('*') ? searchTerm : '*' + searchTerm;

      const filtered = distinct.filter(d => matcher.isMatch(d, searchTerm));
      return suggestions.filter((s: Tag) => filtered.indexOf(s.name) !== -1);
    }
    return [];
  }

  private outersect<T, U>(a: T[], b: T[], mapFn: (value: T, index: number, array: T[]) => U): U[] {
    return a.map(mapFn).filter(value => b.map(mapFn).indexOf(value) === -1);
  }
}