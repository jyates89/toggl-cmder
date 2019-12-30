from requests.auth import HTTPBasicAuth
import requests, json

from toggl.decoders import workspace_decoder

from toggl.decoders import project_decoder
from toggl.encoders import project_encoder

from toggl.decoders import tag_decoder
from toggl.encoders import tag_encoder

from toggl.decoders import time_entry_decoder
from toggl.encoders import time_entry_encoder
from toggl.types import time_entry, workspace, user

from toggl.decoders import user_decoder

class Interface(object):
    def __init__(self, **kwargs):
        super(Interface, self).__init__()

        self.__logger = kwargs.get('logger')
        self.__auth = HTTPBasicAuth(kwargs['api_token'], 'api_token')

    def test_connection(self):
        reply = requests.get(user.User.api_url(),
                             auth=self.__auth)
        if reply.reason == 'Forbidden':
            return False
        return True

    def reset_user_token(self):
        reply = requests.post(user.User.api_token_reset_url(),
                              auth=self.__auth)
        reply.raise_for_status()
        return reply.text

    def download_user_data(self):
        reply = requests.get(
            Users.api_user_url(),
            auth=self.__auth)
        reply.raise_for_status()
        with open('cache.json', 'w') as cache:
            cache.writelines(reply.text)

        return json.loads(reply.text,
                          cls=user_decoder.UserDecoder)

    def load_cached_user_data(self):
        with open('cache.json', 'r') as cache:
            return json.load(cache, cls=user_decoder.UserDecoder)

    def download_workspaces(self):
        reply =  requests.get(workspace.Workspace.api_url(),
                              auth=self.__auth)
        reply.raise_for_status()
        return json.loads(reply.text,
                          cls=workspace_decoder.WorkspaceDecoder)

    def download_projects(self, incoming_workspace):
        reply = requests.get(incoming_workspace.projects_url,
                             auth=self.__auth)
        reply.raise_for_status()
        projects = []
        for project in json.loads(reply.text,
                                  cls=project_decoder.ProjectDecoder):
            project.workspace = incoming_workspace
            projects.append(project)

        return projects

    def download_tags(self, incoming_workspace):
        reply = requests.get(incoming_workspace.tags_url,
                             auth=self.__auth)
        reply.raise_for_status()
        tags = []
        for tag in json.loads(reply.text,
                              cls=tag_decoder.TagDecoder):
            tag.workspace = incoming_workspace
            tags.append(tag)

        return tags

    def get_current_entry(self):
        reply = requests.get(time_entry.TimeEntry.api_current_entry_url(),
                             auth=self.__auth)
        reply.raise_for_status()
        return json.loads(reply.text,
                          cls=time_entry_decoder.TimeEntryDecoder)

    def download_time_entries(self, start, end):
        request_string = time_entry.TimeEntry.api_url() +\
            "?start_date={}&".format(start) +\
            "end_date={}".format(end)
        reply = requests.get(request_string)
        return json.loads(reply.text,
                          cls=time_entry_decoder.TimeEntryDecoder)

    def create_project(self, project):
        data = json.dumps(project, cls=project_encoder.ProjectEncoder)
        result = requests.post(project.api_url(),
                               data=data,
                               auth=self.__auth)
        result.raise_for_status()

    def create_tag(self, tag):
        data = json.dumps(tag, cls=tag_encoder.TagEncoder)
        result = requests.post(tag.api_url(),
                               data=data,
                               auth=self.__auth)
        result.raise_for_status()

    def start_time_entry(self, time_entry):
        data = json.dumps(time_entry, cls=time_entry_encoder.TimeEntryEncoder)
        self.__logger.debug("request.json: {}".format(data))
        result = requests.post(time_entry.api_start_entry_url(),
                               data=data,
                               auth=self.__auth)
        self.__logger.debug("reply.text: {}".format(result.text))
        result.raise_for_status()

    def stop_time_entry(self, time_entry):
        result = requests.put(time_entry.api_stop_entry_url(),
                              auth=self.__auth)
        result.raise_for_status()
