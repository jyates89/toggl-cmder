
from toggl import project

class Workspace(object):
    QUERY_API_URL = "https://www.toggl.com/api/v8/workspaces"
    QUERY_PROJECTS = QUERY_API_URL + "{}/projects"

    def __init__(self, **kwargs):
        self.__id = kwargs.get('id')
        self.__name = kwargs.get('name')

        self.__projects = kwargs.get('projects', [None])
        self.__tags = kwargs.get('tags', [None])
        self.__time_entries = kwargs.get('time_entries', [None])

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    def get_new(self):
        pass

    def get_existing(self):
        pass
