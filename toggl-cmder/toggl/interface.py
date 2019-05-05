from requests.auth import HTTPBasicAuth
import requests, json

from toggl import workspace_decoder
from toggl import workspace

from toggl import project_decoder
from toggl import project

from toggl import tag_decoder
from toggl import tag

from toggl import time_entry_decoder
from toggl import time_entry

class Interface(object):
    def __init__(self, **kwargs):
        super(Interface, self).__init__()

        self.__auth = HTTPBasicAuth(kwargs['api_token'], 'api_token')

    def download_workspaces(self):
        reply =  requests.get(workspace.Workspace.QUERY_API_URL,
                            auth=self.__auth)
        return json.loads(reply.text,
                          cls=workspace_decoder.WorkspaceResponseDecoder)

    def download_projects(self, incoming_workspace):
        reply = requests.get(workspace.Workspace.QUERY_PROJECTS.format(incoming_workspace.id),
                             auth=self.__auth)
        projects = []
        for project in json.loads(reply.text,
                            cls=project_decoder.ProjectResponseDecoder):
            project.workspace = incoming_workspace
            projects.append(project)

        return projects

    def download_tags(self):
        pass

    def download_time_entries(self):
        pass

    def create_workspace(self):
        pass

    def create_project(self):
        pass

    def create_tag(self):
        pass

    def start_time_entry(self):
        pass

    def stop_time_entry(self):
        pass
