
from toggl import project

class Workspace(object):
    WORKSPACE_API_URL = "https://www.toggl.com/api/v8/workspaces"

    def __init__(self, **kwargs):
        self.__id = kwargs.get('id')
        self.__name = kwargs.get('name')

        self.__projects = kwargs.get('projects', [None])
        self.__tags = kwargs.get('tags', [None])
        self.__time_entries = kwargs.get('time_entries', [None])

        self.__QUERY_API_URL = self.WORKSPACE_API_URL + "/{}".format(
            self.__id
        )


    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def projects_url(self):
        return self.__QUERY_API_URL + "/projects"

    @property
    def tags_url(self):
        return self.__QUERY_API_URL + "/tags"
