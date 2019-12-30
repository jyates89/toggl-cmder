from __future__ import annotations
from datetime import datetime
from pytz import timezone

from toggl.types.project import Project


class ProjectBuilder(object):
    def __init__(self):
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

    def last_updated(self, last_update: str) -> ProjectBuilder:
        if last_update is not None:
            try:
                self.__last_updated = datetime.strptime(last_update, '%Y-%m-%dT%H:%M:%S%z')
            except ValueError:
                # try and see if timezone if UTC
                self.__last_updated = datetime.strptime(last_update, '%Y-%m-%dT%H:%M:%S.%fZ')\
                    .replace(tzinfo=timezone('UTC'))
        return self


    def created(self, created: str) -> ProjectBuilder:
        if created is not None:
            self.__created, = datetime.strptime(created, '%Y-%m-%dT%H:%M:%S%z'),
        return self

    def build(self) -> Project:
        return Project(
            identifier=self.__identifier,
            name=self.__name,
            workspace_identifier=self.__workspace_identifier,
            color=self.__color,
            last_updated=self.__last_updated,
            created=self.__created)
