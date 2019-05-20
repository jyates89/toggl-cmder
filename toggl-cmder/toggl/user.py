import re

class User(object):
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

    def find_tag(self, tag_name):
        return filter(
            lambda tag: re.search(tag_name,
                                  tag.name,
                                  re.IGNORECASE),
            self.__tags)

    @property
    def projects(self):
        return self.__projects

    def find_project(self, project_name, workspace_name):
        workspace = self.find_workspace(workspace_name)
        return filter(
            lambda project: re.search(project_name,
                                      project.name,
                                      re.IGNORECASE),
            self.__projects)

    @property
    def time_entries(self):
        return self.__time_entries

    def find_time_entry(self, time_entry_description):
        return filter(
            lambda entry: re.search(time_entry_description,
                                    entry.description,
                                    re.IGNORECASE),
            self.__time_entries)

    @property
    def workspaces(self):
        return self.__workspaces

    def find_workspace(self, workspace_name):
        return filter(
            lambda ws: re.search(workspace_name,
                                 ws.name,
                                 re.IGNORECASE),
            self.__workspaces)

    @staticmethod
    def api_url():
        return "https://www.toggl.com/api/v8/me"

    @staticmethod
    def api_user_url():
        return User.api_url() + "?with_related_data=true"

    @staticmethod
    def api_token_reset_url():
        return "https://www.toggl.com/api/v8/reset_token"
