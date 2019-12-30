from typing import List

import requests, json
from requests.auth import HTTPBasicAuth

from toggl.endpoints.api import API

from toggl.types.user import User
from toggl.decoders.user_decoder import UserDecoder

from toggl.types.workspace import Workspace
from toggl.decoders.workspace_decoder import WorkspaceDecoder

from toggl.types.tag import Tag
from toggl.decoders.tag_decoder import TagDecoder

from toggl.types.project import Project
from toggl.types.time_entry import TimeEntry

class Downloader(object):
    def __init__(self, auth: str):
        self.__auth = HTTPBasicAuth(auth, 'api_token')

    def download_user_data(self) -> User:
        reply = requests.get(
            API().users.details(),
            auth=self.__auth)
        reply.raise_for_status()
        return json.loads(reply.text,
                          cls=UserDecoder)

    def download_workspaces(self) -> List[Workspace]:
        reply = requests.get(
            API().workspaces,
            auth=self.__auth)
        reply.raise_for_status()
        return json.loads(reply.text,
                          cls=WorkspaceDecoder)

    def download_tags(self, workspace: Workspace) -> List[Tag]:
        reply = requests.get(
            API().workspaces.tags(workspace.identifier),
            auth=self.__auth)
        reply.raise_for_status()
        return json.loads(reply.text,
                          cls=TagDecoder)

    def download_projects(self, workspace: Workspace) -> List[Project]:
        pass

    def download_time_entries(self, project: Project) -> List[TimeEntry]:
        pass
