from datetime import datetime, timezone

class TimeEntry(object):
    def __init__(self, **kwargs):
        self.__id = kwargs.get('id')
        self.__workspace_id = kwargs.get('wid')

        self.__project_id = kwargs.get('pid')
        self.__description = kwargs.get('description')

        self.__start_time, = datetime.fromisoformat(kwargs.get('start')),

        self.__duration = kwargs.get('duration', 0)
        self.__is_running = True if self.__duration < 0 else False

        if self.__is_running:
            self.__duration = datetime.now(timezone.utc).timestamp() + self.__duration

        try:
            self.__stop_time, = datetime.strptime(kwargs.get('stop'),
                                                  '%Y-%m-%dT%H:%M:%S%z'),
        except TypeError:
            self.__stop_time = None

        self.__tags = kwargs.get('tags', [])

    @staticmethod
    def entry_api_url():
        return "https://www.toggl.com/api/v8/time_entries"

    @staticmethod
    def entry_start_api_url():
        return TimeEntry.entry_api_url() + "/start"

    def entry_stop_api_url(self):
        return self.entry_api_url() + "/{}/stop".format(
            self.__id
        )

    def entry_details_api_url(self):
        return self.entry_api_url() + "/{}".format(
            self.__id
        )

    @staticmethod
    def current_entry_api_url():
        return TimeEntry.entry_api_url() + "/current"


    @property
    def id(self):
        return self.__id

    @property
    def workspace_id(self):
        return self.__workspace_id

    @property
    def project_id(self):
        return self.__project_id

    @property
    def description(self):
        return self.__description

    @property
    def start_time(self):
        return self.__start_time

    @property
    def stop_time(self):
        return self.__stop_time

    @property
    def duration(self):
        return self.__duration

    @property
    def is_running(self):
        return self.__is_running

    @property
    def tags(self):
        return self.__tags
