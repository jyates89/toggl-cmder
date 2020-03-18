from json import JSONDecoder

from togglcmder.toggl.builders.time_entry_builder import TimeEntryBuilder


class TimeEntryDecoder(JSONDecoder):
    def __init__(self, *args: tuple, **kwargs: dict):
        JSONDecoder.__init__(self,
                             object_hook=TimeEntryDecoder.object_hook,
                             *args,
                             **kwargs)

    @staticmethod
    def object_hook(obj: dict):
        if 'data' in obj:
            return obj['data']

        if 'id' in obj:
            return TimeEntryBuilder()\
                .identifier(obj['id'])\
                .description(obj.get('description', None))\
                .workspace_identifier(obj['wid'])\
                .project_identifier(obj.get('pid', None))\
                .start_time(start_time=obj['start'])\
                .duration(obj.get('duration', None))\
                .stop_time(stop_time=obj.get('stop', None))\
                .tags(obj.get('tags', None))\
                .last_updated(last_update=obj.get('at', None))\
                .build()

        return obj
