

class Workspace(object):
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

    @staticmethod
    def api_url():
        return "https://www.toggl.com/api/v8/workspaces"

    @property
    def projects_url(self):
        return Workspace.api_url() + "/{}/projects".format(
            self.__id
        )

    @property
    def tags_url(self):
        return Workspace.api_url() + "/{}/tags".format(
            self.__id
        )

    def __str__(self):
        return "{}".format(
            self.__name
        )
