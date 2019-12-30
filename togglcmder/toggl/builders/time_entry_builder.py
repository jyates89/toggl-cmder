from __future__ import annotations

from datetime import datetime
from pytz import timezone
from typing import List

from toggl.types.time_entry import TimeEntry


class TimeEntryBuilder(object):
    def __init__(self):
        self.__identifier = None
        self.__description = None
        self.__project_identifier = None
        self.__workspace_identifier = None
        self.__start_time = None
        self.__duration = None
        self.__stop_time = None
        self.__tags = None
        self.__last_updated = None

    def identifier(self, identifier: int) -> TimeEntryBuilder:
        self.__identifier = identifier
        return self

    def description(self, description: str) -> TimeEntryBuilder:
        self.__description = description
        return self

    def project_identifier(self, project_identifier: int) -> TimeEntryBuilder:
        self.__project_identifier = project_identifier
        return self

    def workspace_identifier(self, workspace_identifier: int) -> TimeEntryBuilder:
        self.__workspace_identifier = workspace_identifier
        return self

    def start_time(self, start_time: str) -> TimeEntryBuilder:
        if start_time is not None:
            try:
                self.__start_time = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S%z')
            except ValueError:
                # try and see if timezone if UTC
                self.__start_time = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S.%fZ')\
                    .replace(tzinfo=timezone('UTC'))
        return self

    def duration(self, duration: int) -> TimeEntryBuilder:
        if duration < 0:
            self.__duration = datetime.now(timezone('UTC')).replace(microsecond=0).timestamp() + duration
        else:
            self.__duration = duration
        return self

    def stop_time(self, stop_time: str) -> TimeEntryBuilder:
        if stop_time is not None:
            try:
                self.__stop_time = datetime.strptime(stop_time, '%Y-%m-%dT%H:%M:%S%z')
            except ValueError:
                # try and see if timezone if UTC
                self.__stop_time = datetime.strptime(stop_time, '%Y-%m-%dT%H:%M:%S.%fZ')\
                    .replace(tzinfo=timezone('UTC'))
        return self

    def tags(self, tags: List[str]) -> TimeEntryBuilder:
        self.__tags = tags
        return self

    def last_updated(self, last_update: str) -> TimeEntryBuilder:
        if last_update is not None:
            try:
                self.__last_updated = datetime.strptime(last_update, '%Y-%m-%dT%H:%M:%S%z')
            except ValueError:
                # try and see if timezone if UTC
                self.__last_updated = datetime.strptime(last_update, '%Y-%m-%dT%H:%M:%S.%fZ')\
                    .replace(tzinfo=timezone('UTC'))
        return self

    def build(self) -> TimeEntry:
        return TimeEntry(
            identifier=self.__identifier,
            description=self.__description,
            project_identifier=self.__project_identifier,
            workspace_identifier=self.__workspace_identifier,
            start_time=self.__start_time,
            duration=self.__duration,
            stop_time=self.__stop_time,
            tags=self.__tags,
            last_updated=self.__last_updated)
