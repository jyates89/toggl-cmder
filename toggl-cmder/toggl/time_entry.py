from datetime import datetime

class TimeEntry(object):

    def __init__(self, **kwargs):
        self.__id = kwargs.get('id')
        self.__workspace_id = kwargs.get('wid')
        self.__project_id = kwargs.get('pid')

        self.__description = kwargs.get('description')

        self.__start_time, = datetime.strptime(kwargs.get('start'),
                                               '%Y-%m-%dT%H:%M:%S%z'),

        self.__is_running = False

        try:
            self.__stop_time, = datetime.strptime(kwargs.get('stop'),
                                                  '%Y-%m-%dT%H:%M:%S%z'),
        except ValueError:
            self.__stop_time = None

        self.__duration = kwargs.get('duration')

        self.__tags = kwargs.get('tags', [])

    def entry_api_url(self):
        return "https://www.toggl.com/api/v8/time_entries"

    def entry_start_api_url(self):
        return self.entry_api_url() + "/start"

    def entry_stop_api_url(self):
        return self.entry_api_url() + "/{}/stop".format(
            self.__id
        )

    def entry_details_api_url(self):
        return self.entry_api_url() + "/{}".format(
            self.__id
        )

    def current_entry_api_url(self):
        return self.entry_api_url() + "/current"


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
    def tags(self):
        return self.__tags
