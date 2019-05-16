
from toggl import time_entry

class TimeEntryBuilder(object):

    @staticmethod
    def from_now(workspace_id, project_id):
        return time_entry.TimeEntry(
            id=None,

        )

    @staticmethod
    def from_start(start, workspace_id, project_id):
        pass
