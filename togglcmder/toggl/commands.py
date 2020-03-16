import requests
from requests.auth import HTTPBasicAuth
import json
import logging
from typing import List

from togglcmder.toggl.endpoints.api import API

from togglcmder.toggl.types.project import Project
from togglcmder.toggl.encoders.project_encoder import ProjectEncoder
from togglcmder.toggl.decoders.project_decoder import ProjectDecoder

from togglcmder.toggl.types.tag import Tag
from togglcmder.toggl.encoders.tag_encoder import TagEncoder
from togglcmder.toggl.decoders.tag_decoder import TagDecoder

from togglcmder.toggl.types.time_entry import TimeEntry
from togglcmder.toggl.encoders.time_entry_encoder import TimeEntryEncoder
from togglcmder.toggl.decoders.time_entry_decoder import TimeEntryDecoder


class Commands(object):
    def __init__(self, auth: str):
        self.__auth = HTTPBasicAuth(auth, 'api_token')

    @staticmethod
    def __log_command(logger: logging.Logger, result: requests.Response):
        logger.debug(result.request.body)
        logger.debug(result.text)

    def add_tag(self, tag: Tag) -> Tag:
        result = requests.post(
            API().tags,
            data=json.dumps(tag,
                            cls=TagEncoder),
            auth=self.__auth)

        Commands.__log_command(logging.getLogger(__name__), result)

        result.raise_for_status()
        return json.loads(result.text,
                          cls=TagDecoder)

    def delete_tag(self, tag: Tag) -> None:
        result = requests.delete(
            API().tags.details(tag.identifier),
            auth=self.__auth
        )

        Commands.__log_command(logging.getLogger(__name__), result)

        result.raise_for_status()

    def update_tag(self, tag: Tag) -> Tag:
        result = requests.put(
            API().tags.details(tag.identifier),
            data=json.dumps(tag,
                            cls=TagEncoder),
            auth=self.__auth
        )

        Commands.__log_command(logging.getLogger(__name__), result)

        result.raise_for_status()
        return json.loads(result.text,
                          cls=TagDecoder)

    def add_project(self, project: Project) -> Project:
        result = requests.post(
            API().projects,
            data=json.dumps(project,
                            cls=ProjectEncoder),
            auth=self.__auth)

        Commands.__log_command(logging.getLogger(__name__), result)

        result.raise_for_status()
        return json.loads(result.text,
                          cls=ProjectDecoder)

    def delete_project(self, project: Project) -> None:
        result = requests.delete(
            API().projects.details(project.identifier),
            auth=self.__auth
        )

        Commands.__log_command(logging.getLogger(__name__), result)

        result.raise_for_status()

    def delete_projects(self, projects: List[Project]) -> None:
        result = requests.delete(
            API().projects.details(
                identifiers=[project.identifier for project in projects]
            ),
            auth=self.__auth
        )

        Commands.__log_command(logging.getLogger(__name__), result)

        result.raise_for_status()

    def update_project(self, project: Project) -> Project:
        result = requests.put(
            API().projects.details(project.identifier),
            data=json.dumps(project,
                            cls=ProjectEncoder),
            auth=self.__auth
        )

        Commands.__log_command(logging.getLogger(__name__), result)

        result.raise_for_status()
        return json.loads(result.text,
                          cls=ProjectDecoder)

    def start_time_entry(self, time_entry: TimeEntry) -> TimeEntry:
        result = requests.post(
            API().time_entries.start(),
            data=json.dumps(time_entry,
                            cls=TimeEntryEncoder),
            auth=self.__auth
        )

        Commands.__log_command(logging.getLogger(__name__), result)

        result.raise_for_status()
        return json.loads(result.text,
                          cls=TimeEntryDecoder)

    def stop_time_entry(self, time_entry: TimeEntry) -> TimeEntry:
        result = requests.put(
            API().time_entries.stop(time_entry.identifier),
            auth=self.__auth
        )

        Commands.__log_command(logging.getLogger(__name__), result)

        result.raise_for_status()
        return json.loads(result.text,
                          cls=TimeEntryDecoder)

    def add_completed_time_entry(self, time_entry: TimeEntry) -> TimeEntry:
        result = requests.post(
            API().time_entries,
            data=json.dumps(time_entry,
                            cls=TimeEntryEncoder),
            auth=self.__auth
        )

        Commands.__log_command(logging.getLogger(__name__), result)

        result.raise_for_status()
        return json.loads(result.text,
                          cls=TimeEntryDecoder)

    def update_completed_time_entry(self, time_entry: TimeEntry) -> TimeEntry:
        result = requests.put(
            API().time_entries.details(time_entry.identifier),
            data=json.dumps(time_entry,
                            cls=TimeEntryEncoder),
            auth=self.__auth
        )

        Commands.__log_command(logging.getLogger(__name__), result)

        result.raise_for_status()
        return json.loads(result.text,
                          cls=TimeEntryDecoder)

    def delete_time_entry(self, time_entry: TimeEntry) -> None:
        result = requests.delete(
            API().time_entries.details(time_entry.identifier),
            auth=self.__auth
        )

        Commands.__log_command(logging.getLogger(__name__), result)

        result.raise_for_status()

    def reset_api_token(self) -> str:
        reply = requests.post(API().users.reset_api_token(),
                              auth=self.__auth
                              )
        reply.raise_for_status()
        return reply.text
