from requests.auth import HTTPBasicAuth
import requests, json

from toggl import workspace_decoder
from toggl import workspace

from toggl import project_decoder
from toggl import project

from toggl import tag_decoder
from toggl import tag

from toggl import time_entry_decoder
from toggl import time_entry_encoder
from toggl import time_entry

class Interface(object):
    def __init__(self, **kwargs):
        super(Interface, self).__init__()

        self.__auth = HTTPBasicAuth(kwargs['api_token'], 'api_token')

    def download_workspaces(self):
        reply =  requests.get(workspace.Workspace.WORKSPACE_API_URL,
                            auth=self.__auth)
        return json.loads(reply.text,
                          cls=workspace_decoder.WorkspaceResponseDecoder)

    def download_projects(self, incoming_workspace):
        reply = requests.get(incoming_workspace.projects_url,
                             auth=self.__auth)
        projects = []
        for project in json.loads(reply.text,
                                  cls=project_decoder.ProjectResponseDecoder):
            project.workspace = incoming_workspace
            projects.append(project)

        return projects

    def download_tags(self, incoming_workspace):
        reply = requests.get(incoming_workspace.tags_url,
                             auth=self.__auth)
        tags = []
        for tag in json.loads(reply.text,
                              cls=tag_decoder.TagResponseDecoder):
            tag.workspace = incoming_workspace
            tags.append(tag)

        return tags

    def download_time_entries(self, incoming_workspace,
                              incoming_project, incoming_tags):
        pass

    def create_project(self):
        pass

    def create_tag(self):
        pass

    def create_time_entry(self, incoming_workspace,
                          incoming_project, incoming_tags,
                          description):
        entry = time_entry.TimeEntry.fromComponents(
            incoming_workspace, incoming_project,
            incoming_tags, description,
        )
        print(json.dumps(entry, cls=time_entry_encoder.TimeEntryEncoder))

    def start_time_entry(self):
        pass

    def stop_time_entry(self):
        pass
