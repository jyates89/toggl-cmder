from __future__ import annotations
from datetime import datetime
from tzlocal import get_localzone
from typing import Optional

from togglcmder.toggl.types.project import Project


class ProjectBuilder(object):
    def __init__(self, project: Optional[Project] = None):
        if project is not None:
            self.__identifier = project.identifier
            self.__name = project.name
            self.__workspace_identifier = project.workspace_identifier
            self.__color = project.color
            self.__last_updated = project.last_updated
            self.__created = project.created
        else:
            self.__identifier = None
            self.__name = None
            self.__workspace_identifier = None
            self.__color = None
            self.__last_updated = None
            self.__created = None

    def identifier(self, identifier: int) -> ProjectBuilder:
        self.__identifier = identifier
        return self

    def name(self, name: str) -> ProjectBuilder:
        self.__name = name
        return self

    def workspace_identifier(self, workspace_identifier: int) -> ProjectBuilder:
        self.__workspace_identifier = workspace_identifier
        return self

    def color(self, color: int) -> ProjectBuilder:
        self.__color = Project.Color(color)
        return self

    def last_updated(self, *, last_update: Optional[str] = None,
                     epoch: Optional[int] = None) -> ProjectBuilder:
        if last_update:
            self.__last_updated = self.__datetime_from_str(last_update)
        elif epoch:
            self.__last_updated = self.__datetime_from_timestamp(epoch)
        return self

    def created(self, *, created: Optional[str] = None,
                epoch: Optional[int] = None) -> ProjectBuilder:
        if created:
            self.__created = self.__datetime_from_str(created)
        elif epoch:
            self.__created = self.__datetime_from_timestamp(epoch)
        return self

    def build(self) -> Project:
        return Project(
            identifier=self.__identifier,
            name=self.__name,
            workspace_identifier=self.__workspace_identifier,
            color=self.__color,
            last_updated=self.__last_updated,
            created=self.__created)

    @staticmethod
    def __datetime_from_str(date: str) -> datetime:
        parsed_date = datetime.fromisoformat(date.replace('Z', '+00:00'))
        if not parsed_date.tzinfo:
            return get_localzone().localize(parsed_date)
        return parsed_date.astimezone(get_localzone())

    @staticmethod
    def __datetime_from_timestamp(timestamp: int) -> datetime:
        return get_localzone().localize(datetime.fromtimestamp(timestamp))
