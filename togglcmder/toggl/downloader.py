from typing import List

import requests, json
from requests.auth import HTTPBasicAuth
from datetime import datetime
import logging

from togglcmder.toggl.endpoints.api import API

from togglcmder.toggl.types.user import User
from togglcmder.toggl.decoders.user_decoder import UserDecoder

from togglcmder.toggl.types.workspace import Workspace
from togglcmder.toggl.decoders.workspace_decoder import WorkspaceDecoder

from togglcmder.toggl.types.tag import Tag
from togglcmder.toggl.decoders.tag_decoder import TagDecoder

from togglcmder.toggl.types.project import Project
from togglcmder.toggl.decoders.project_decoder import ProjectDecoder

from togglcmder.toggl.types.time_entry import TimeEntry
from togglcmder.toggl.decoders.time_entry_decoder import TimeEntryDecoder

class Downloader(object):
    def __init__(self, auth: str):
        self.__auth = HTTPBasicAuth(auth, 'api_token')

    @staticmethod
    def __log_download(logger: logging.Logger, result: requests.Response):
        logger.debug(result.request.body)
        logger.debug(result.text)

    def download_user_data(self) -> User:
        reply = requests.get(
            API().users.details(),
            auth=self.__auth
        )

        # Commented this out because it may show sensitive information.
        # Downloader.__log_download(logging.getLogger(__name__), reply)

        reply.raise_for_status()
        return json.loads(reply.text,
                          cls=UserDecoder)

    def download_workspaces(self) -> List[Workspace]:
        reply = requests.get(
            API().workspaces,
            auth=self.__auth
        )

        Downloader.__log_download(logging.getLogger(__name__), reply)

        reply.raise_for_status()
        return json.loads(reply.text,
                          cls=WorkspaceDecoder)

    def download_tags(self, workspace: Workspace) -> List[Tag]:
        reply = requests.get(
            API().workspaces.tags(workspace.identifier),
            auth=self.__auth
        )

        Downloader.__log_download(logging.getLogger(__name__), reply)

        reply.raise_for_status()
        return json.loads(reply.text,
                          cls=TagDecoder)

    def download_projects(self, workspace: Workspace) -> List[Project]:
        reply = requests.get(
            API().workspaces.projects(workspace.identifier),
            auth=self.__auth
        )

        Downloader.__log_download(logging.getLogger(__name__), reply)

        reply.raise_for_status()
        return json.loads(reply.text,
                          cls=ProjectDecoder)

    def download_time_entries(self, start: datetime, end: datetime) -> List[TimeEntry]:
        reply = requests.get(
            API().time_entries.search(start, end),
            auth=self.__auth
        )

        Downloader.__log_download(logging.getLogger(__name__), reply)

        reply.raise_for_status()
        return json.loads(reply.text,
                          cls=TimeEntryDecoder)

    def get_current_time_entry(self) -> TimeEntry:
        result = requests.get(
            API().time_entries.current(),
            auth=self.__auth
        )

        Downloader.__log_download(logging.getLogger(__name__), result)

        result.raise_for_status()
        return json.loads(result.text,
                          cls=TimeEntryDecoder)
