
from toggl import time_entry

class TimeEntryBuilder(object):
    def __init__(self, **kwargs):
        pass

    def get_current(self):
        return time_entry.TimeEntry()

    def get_new(self, **kwargs):
        return time_entry.TimeEntry()
