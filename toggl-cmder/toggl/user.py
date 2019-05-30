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

    def find_tag(self, tag_name, workspace_name):
        workspace = self.find_workspace(workspace_name)
        tag = next(filter(
            lambda tag: re.search(tag_name,
                                  tag.name,
                                  re.IGNORECASE)
                and tag.workspace_id == workspace.id,
            self.__tags), None)
        if tag is None:
            raise ValueError("no tag matching '{}' found in workspace matching '{}'".format(
                tag_name, workspace_name
            ))

        return tag

    def find_user_tag(self, tag_name):
        return next(filter(
            lambda tag: re.search(tag_name,
                                  tag.name,
                                  re.IGNORECASE),
            self.__tags), None)

    @property
    def projects(self):
        return self.__projects

    def get_project_from_id(self, id):
        return next(filter(
            lambda project: project.id == id,
            self.__projects
        ))

    def find_project(self, project_name, workspace_name):
        workspace = self.find_workspace(workspace_name)
        project = next(filter(
            lambda project: re.search(project_name,
                                      project.name,
                                      re.IGNORECASE)
                and project.workspace_id == workspace.id,
            self.__projects), None)
        if project is None:
            raise ValueError("no project matching '{}' found in workspace matching '{}'".format(
                project_name, workspace_name
            ))
        return project

    def find_user_project(self, project_name):
        return next(filter(
            lambda project: re.search(project_name,
                                      project.name,
                                      re.IGNORECASE),
            self.__projects), None)

    @property
    def time_entries(self):
        return self.__time_entries

    def find_time_entry(self, time_entry_description, workspace_name, project_name):
        project = self.find_project(project_name, workspace_name)
        time_entry = next(filter(
            lambda entry: re.search(time_entry_description,
                                    entry.description,
                                    re.IGNORECASE)
                and entry.project_id == project.id,
            self.__time_entries), None)
        if time_entry is None:
            raise ValueError("no time entry with description matching '{}' found for "
                             "project matching '{}' in workspace matching '{}'".format(
                time_entry_description, project_name, workspace_name
            ))
        return time_entry

    def find_user_time_entry(self, time_entry_description):
        return next(filter(
            lambda entry: re.search(time_entry_description,
                                    entry.description,
                                    re.IGNORECASE),
            self.__time_entries), None)

    @property
    def workspaces(self):
        return self.__workspaces

    def get_workspace_from_id(self, id):
        return next(filter(
            lambda workspace: workspace.id == id,
            self.__workspaces
        ))

    def find_workspace(self, workspace_name):
        workspace = next(filter(
            lambda ws: re.search(workspace_name,
                                 ws.name,
                                 re.IGNORECASE),
            self.__workspaces), None)
        if workspace is None:
            raise ValueError("no workspace matching '{}' found".format(
                workspace_name
            ))
        return workspace

    @staticmethod
    def api_url():
        return "https://www.toggl.com/api/v8/me"

    @staticmethod
    def api_user_url():
        return User.api_url() + "?with_related_data=true"

    @staticmethod
    def api_token_reset_url():
        return "https://www.toggl.com/api/v8/reset_token"
