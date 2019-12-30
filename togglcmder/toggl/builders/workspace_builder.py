from __future__ import annotations
from datetime import datetime
from pytz import timezone

from toggl.types.workspace import Workspace

class WorkspaceBuilder(object):
    def __init__(self):
        self.__identifier = None
        self.__name = None
        self.__last_updated = None

    def identifier(self, identifier: int) -> WorkspaceBuilder:
        self.__identifier = identifier
        return self

    def name(self, name: str) -> WorkspaceBuilder:
        self.__name = name
        return self

    def last_updated(self, last_update: str) -> WorkspaceBuilder:
        if last_update is not None:
            try:
                self.__last_updated = datetime.strptime(last_update, '%Y-%m-%dT%H:%M:%S%z')
            except ValueError:
                # try and see if timezone if UTC
                self.__last_updated = datetime.strptime(last_update, '%Y-%m-%dT%H:%M:%S.%fZ')\
                    .replace(tzinfo=timezone('UTC'))
        return self

    def build(self) -> Workspace:
        return Workspace(
            identifier=self.__identifier,
            name=self.__name,
            last_updated=self.__last_updated)
