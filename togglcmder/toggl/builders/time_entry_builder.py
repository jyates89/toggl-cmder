from __future__ import annotations

from datetime import datetime
from pytz import timezone
from tzlocal import get_localzone
from typing import List, Optional

from togglcmder.toggl.types.time_entry import TimeEntry


class TimeEntryBuilder(object):
    def __init__(self, time_entry: Optional[TimeEntry] = None):
        if time_entry is not None:
            self.__identifier = time_entry.identifier
            self.__description = time_entry.description
            self.__project_identifier = time_entry.project_identifier
            self.__workspace_identifier = time_entry.workspace_identifier
            self.__start_time = time_entry.start_time
            self.__duration = time_entry.duration
            self.__stop_time = time_entry.stop_time
            self.__tags = time_entry.tags
            self.__last_updated = time_entry.last_updated
        else:
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

    def start_time(self, *, start_time: Optional[str] = None, epoch: Optional[int] = None,
                   dt: Optional[datetime] = None) -> TimeEntryBuilder:
        if start_time is not None:
            self.__start_time = self.__datetime_from_str(start_time)
        elif epoch is not None:
            self.__start_time = self.__datetime_from_timestamp(epoch)
        elif dt is not None:
            self.__start_time = dt
        return self

    def duration(self, duration: int) -> TimeEntryBuilder:
        if duration < 0:
            self.__duration = datetime.now(timezone('UTC')).replace(microsecond=0).timestamp() + duration
        else:
            self.__duration = duration
        return self

    def stop_time(self, *, stop_time: Optional[str] = None, epoch: Optional[int] = None,
                  dt: Optional[datetime] = None) -> TimeEntryBuilder:
        if stop_time is not None:
            self.__stop_time = self.__datetime_from_str(stop_time)
        elif epoch is not None:
            self.__stop_time = self.__datetime_from_timestamp(epoch)
        elif dt is not None:
            self.__stop_time = dt
        return self

    def unset_stop_time(self):
        self.__stop_time = None

    def unset_duration(self):
        self.__duration = None

    def tags(self, tags: List[str]) -> TimeEntryBuilder:
        self.__tags = tags
        return self

    def add_tags(self, tags: List[str]) -> TimeEntryBuilder:
        self.__tags.extend(tags)
        return self

    def remove_tags(self, tags: List[str]) -> TimeEntryBuilder:
        for tag in tags:
            self.__tags.remove(tag)
        return self

    def last_updated(self, *, last_update: Optional[str] = None, epoch: Optional[int] = None) -> TimeEntryBuilder:
        if last_update is not None:
            self.__last_updated = self.__datetime_from_str(last_update)
        elif epoch is not None:
            self.__last_updated = self.__datetime_from_timestamp(epoch)
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

    @staticmethod
    def __datetime_from_str(date: str) -> datetime:
        parsed_date = datetime.fromisoformat(date.replace('Z', '+00:00'))
        if not parsed_date.tzinfo:
            return get_localzone().localize(parsed_date)
        return parsed_date.astimezone(tz=get_localzone())

    @staticmethod
    def __datetime_from_timestamp(timestamp: int) -> datetime:
        return get_localzone().localize(datetime.fromtimestamp(timestamp))
