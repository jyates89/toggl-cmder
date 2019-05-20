from json import JSONDecoder

from toggl import time_entry

class TimeEntryDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        JSONDecoder.__init__(self,
                             object_hook=self.object_hook,
                             *args,
                             **kwargs)

    def object_hook(self, obj):
        if 'data' in obj:
            return obj['data']
        return time_entry.TimeEntry(
            id=obj.get('id'),
            wid=obj.get('wid'),
            pid=obj.get('pid'),
            description=obj.get('description'),
            start=obj.get('start'),
            duration=obj.get('duration'),
            stop=obj.get('stop', None),
            tags=obj.get('tags', [])
        )
