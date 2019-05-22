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
    def api_url():
        return "https://www.toggl.com/api/v8/time_entries"

    @staticmethod
    def api_start_entry_url():
        return TimeEntry.api_url() + "/start"

    def api_stop_entry_url(self):
        return self.api_url() + "/{}/stop".format(
            self.__id
        )

    def api_entry_details_url(self):
        return self.api_url() + "/{}".format(
            self.__id
        )

    @staticmethod
    def api_current_entry_url():
        return TimeEntry.api_url() + "/current"


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

    def __str__(self):
        return "{},{},{},{},{}".format(
            self.__description,
            self.__id,
            self.__project_id,
            self.__workspace_id,
            self.__duration,
        )