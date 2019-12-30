import json

from toggl.types.time_entry import TimeEntry


class TimeEntryEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, TimeEntry):
            entry = {'time_entry': {
                'pid': obj.project_identifier,
                'description': obj.description,
                'start': obj.start_time.isoformat(),
                'tags': obj.tags,
                'created_with': 'toggl_cmder'
            }}
            if obj.duration is not None and obj.duration > 0:
                entry['time_entry']['duration'] = obj.duration
            if obj.stop_time is not None:
                entry['time_entry']['stop'] = obj.stop_time.isoformat()
            return entry
        return super(TimeEntryEncoder, self).default(obj)
