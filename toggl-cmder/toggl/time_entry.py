import time

class TimeEntry(object):
    API_URL = "https://www.toggl.com/api/v8/time_entries"

    def __init__(self, **kwargs):
        super(TimeEntry, self).__init__(kwargs)
        self.__description = kwargs.get('description')
        self.__workspace_id = kwargs.get('workspace_id')
        self.__project_id = kwargs.get('project_id')

        self.__start_time = kwargs.get('start')
        self.__duration = kwargs.get('duration')

        self.__tags = kwargs.get('tags', [None])

        self.__project_ref = kwargs.get('project', None)
        self.__workspace_ref = kwargs.get('workspace', None)

    def start(self):
        pass

    def stop(self):
        pass
