from __future__ import annotations
from datetime import datetime
from tzlocal import get_localzone
from typing import Optional

from togglcmder.toggl.types.workspace import Workspace


class WorkspaceBuilder(object):
    def __init__(self, workspace: Optional[Workspace] = None):
        if workspace is not None:
            self.__identifier = workspace.identifier
            self.__name = workspace.name
            self.__last_updated = workspace.last_updated
        else:
            self.__identifier = None
            self.__name = None
            self.__last_updated = None

    def identifier(self, identifier: int) -> WorkspaceBuilder:
        self.__identifier = identifier
        return self

    def name(self, name: str) -> WorkspaceBuilder:
        self.__name = name
        return self

    def last_updated(self, *, last_update: Optional[str] = None,
                     epoch: Optional[int] = None) -> WorkspaceBuilder:
        if last_update:
            self.__last_updated = self.__datetime_from_str(last_update)
        elif epoch:
            self.__last_updated = self.__datetime_from_timestamp(epoch)
        return self

    def build(self) -> Workspace:
        return Workspace(
            identifier=self.__identifier,
            name=self.__name,
            last_updated=self.__last_updated)

    @staticmethod
    def __datetime_from_str(date: str) -> datetime:
        parsed_date = datetime.fromisoformat(date.replace('Z', '+00:00'))
        if not parsed_date.tzinfo:
            return get_localzone().localize(parsed_date)
        return parsed_date.astimezone(get_localzone())

    @staticmethod
    def __datetime_from_timestamp(timestamp: int) -> datetime:
        return get_localzone().localize(datetime.fromtimestamp(timestamp))
