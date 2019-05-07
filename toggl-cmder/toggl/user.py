
from datetime import datetime

class User(object):
    USER_API_URL = "https://www.toggl.com/api/v8/me"

    def __init__(self, **kwargs):
        self.__since = kwargs.get('since')
        self.__id = kwargs.get('id')
        self.__name = kwargs.get('full_name')

        self.__tags = [] # tag.Tag
        self.__projects = [] # project.Project
        self.__time_entries = [] # time_entry.TimeEntry
        self.__workspaces = [] # workspace.Workspace

    @property
    def member_since(self):
        return self.__since

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

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
