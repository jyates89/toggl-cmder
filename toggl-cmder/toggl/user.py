

class User(object):
    USER_API_URL = "https://www.toggl.com/api/v8/me"
    USER_API_RELATED_DATA_URL = USER_API_URL + \
                                "?with_related_data=true"
    USER_TOKEN_RESET = "https://www.toggl.com/api/v8/reset_token"
    def __init__(self, **kwargs):
        self.__name = kwargs.get('full_name')
        self.__id = kwargs.get('id')
        self.__api_token = kwargs.get('api_token', None)

        self.__tags = kwargs.get('tags', []) # tag.Tag
        self.__projects = kwargs.get('projects', []) # project.Project
        self.__time_entries = kwargs.get('time_entries', []) # time_entry.TimeEntry
        self.__workspaces = kwargs.get('workspaces', []) # workspace.Workspace

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def api_token(self):
        return self.__api_token

    @property
    def tags(self):
        return self.__tags

    @property
    def projects(self):
        return self.__projects

    @property
    def time_entries(self):
        return self.__time_entries

    @property
    def workspaces(self):
        return self.__workspaces
