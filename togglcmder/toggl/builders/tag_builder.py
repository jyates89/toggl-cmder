from __future__ import annotations
from typing import Optional

from togglcmder.toggl.types.tag import Tag


class TagBuilder(object):
    def __init__(self, tag: Optional[Tag] = None):
        if tag is not None:
            self.__identifier = tag.identifier
            self.__name = tag.name
            self.__workspace_identifier = tag.workspace_identifier
        else:
            self.__identifier = None
            self.__name = None
            self.__workspace_identifier = None

    def identifier(self, identifier: int) -> TagBuilder:
        self.__identifier = identifier
        return self

    def name(self, name: str) -> TagBuilder:
        self.__name = name
        return self

    def workspace_identifier(self, workspace_identifier: int) -> TagBuilder:
        self.__workspace_identifier = workspace_identifier
        return self

    def build(self) -> Tag:
        return Tag(
            identifier=self.__identifier,
            name=self.__name,
            workspace_identifier=self.__workspace_identifier)
