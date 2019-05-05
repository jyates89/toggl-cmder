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
        reply =  requests.get(workspace.Workspace.API_URL,
                            auth=self.__auth)
        return json.loads(reply.text,
                          cls=workspace_decoder.WorkspaceResponseDecoder)

    def download_projects(self, workspace):
        reply = request.get(project.Project.API_URL.format(
            workspace=
        ),
                            auth=self.__auth)
        pass

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
