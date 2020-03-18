from enum import Enum, unique
from typing import Optional
from datetime import datetime
from functools import total_ordering


@total_ordering
class Project(object):
    @unique
    class Color(Enum):
        LIGHT_BLUE = 0
        LIGHT_PURPLE = 1
        PINK = 2
        LIGHT_ORANGE = 3
        ORANGE = 4
        LIGHT_GREEN = 5
        CYAN = 6
        PEACH = 7
        BLUE = 8
        PURPLE = 9
        YELLOW = 10
        GREEN = 11
        RED = 12
        BRIGHT_RED = 13
        BLACK = 14

        @staticmethod
        def from_string(string: str):
            return Project.Color[string.upper()]

        def __str__(self):
            return self.name.lower()

    def __init__(self, *, name: str, workspace_identifier: int,
                 color: Optional[Color] = None,
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
        return "{},{},{},{},{},{}".format(
            self.name,
            self.identifier,
            self.last_updated,
            self.workspace_identifier,
            self.color.name,
            self.created)

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
