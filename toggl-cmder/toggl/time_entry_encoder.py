from json import JSONEncoder

from toggl import time_entry

class TimeEntryEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, time_entry.TimeEntry):
            return { 'time_entry' :
                         {
                             'id': o.id,
                             'wid': o.workspace_id,
                             'pid': o.project_id,
                             'description': o.description,
                             'start': o.start_time.isoformat()
                         }}
        return super(TimeEntryEncoder, self).default(o)
