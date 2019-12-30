from enum import Enum, unique
from typing import Optional
from datetime import datetime


class Project(object):
    @unique
    class Color(Enum):
        RED = 1
        GREEN = 2
        BLUE = 3
        YELLOW = 4
        PURPLE = 5
        BLACK = 6

    def __init__(self, *, name: str, workspace_identifier: int,
                 color: Optional[Color] = Color.RED,
                 identifier: Optional[int] = None,
                 last_updated: Optional[datetime] = None,
                 created: Optional[datetime] = None):
        self.__identifier = identifier
        self.__name = name
        self.__workspace_identifier = workspace_identifier
        self.__color = color
        self.__last_updated = last_updated
        self.__created = created

    def __eq__(self, other):
        if not isinstance(other, Project):
            return NotImplemented

        return self.identifier == other.identifier \
               and self.name == other.name \
               and self.workspace_identifier == other.workspace_identifier \
               and self.color == other.color \
               and self.last_updated == other.last_updated \
               and self.created == other.created

    def __lt__(self, other):
        if not isinstance(other, Project):
            return NotImplemented
        return self.__name.lower() < other.name.lower()

    def __str__(self):
        return """
        name = {},
        identifier = {},
        last updated = {},
        workspace identifier = {},
        color = {},
        created = {}
        """.format(
            self.name,
            self.identifier,
            self.last_updated,
            self.workspace_identifier,
            self.color.name,
            self.created
        )

    @property
    def name(self) -> str:
        return self.__name

    @property
    def identifier(self) -> int:
        return self.__identifier

    @property
    def workspace_identifier(self) -> int:
        return self.__workspace_identifier

    @property
    def color(self) -> Color:
        return self.__color

    @property
    def last_updated(self) -> datetime:
        return self.__last_updated

    @property
    def created(self) -> datetime:
        return self.__created
