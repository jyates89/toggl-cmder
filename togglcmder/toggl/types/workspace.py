from typing import Optional
from datetime import datetime
from functools import total_ordering


@total_ordering
class Workspace(object):
    def __init__(self, *, name: str,
                 identifier: Optional[int] = None,
                 last_updated: Optional[datetime] = None):
        self.__name = name
        self.__identifier = identifier
        self.__last_updated = last_updated

    def __eq__(self, other):
        if not isinstance(other, Workspace):
            return NotImplemented

        return self.__name == other.name \
            and self.__identifier == other.identifier \
            and self.__last_updated == other.last_updated

    def __lt__(self, other):
        if not isinstance(other, Workspace):
            return NotImplemented
        return self.__name.lower() < other.__name.lower()

    def __str__(self):
        return "{},{},{}".format(
            self.__name,
            self.__identifier,
            self.__last_updated.isoformat())

    @property
    def name(self) -> str:
        return self.__name

    @property
    def identifier(self) -> int:
        return self.__identifier

    @property
    def last_updated(self) -> datetime:
        return self.__last_updated
