import { Pipe, PipeTransform } from '@angular/core';
import { TagService } from './tag.service';
import { Tag } from './tag';

@Pipe({
  name: 'tagFilter'
})
export class TagFilterPipe implements PipeTransform {

  constructor(private tagService: TagService) { }

  transform(suggestions: Tag[], tags: Tag[],  filter: string): any {
    return this.tagService.filterSuggestions(suggestions, tags, filter);
  }
}