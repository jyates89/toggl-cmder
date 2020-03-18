from typing import Optional
from datetime import datetime
from functools import total_ordering


@total_ordering
class User(object):
    def __init__(self, *, name: str, api_token: str,
                 identifier: Optional[int] = None,
                 last_updated: Optional[datetime] = None):
        self.__name = name
        self.__api_token = api_token
        self.__identifier = identifier
        self.__last_updated = last_updated

    def __eq__(self, other):
        if not isinstance(other, User):
            return NotImplemented

        return self.__name == other.name \
            and self.__api_token == other.api_token \
            and self.__identifier == other.identifier \
            and self.__last_updated == other.last_updated

    def __lt__(self, other):
        if not isinstance(other, User):
            return NotImplemented
        return self.__name.lower() < other.__name.lower()

    def __str__(self):
        return "{},{},{},{}".format(
            self.name,
            self.identifier,
            self.api_token,
            self.last_updated.isoformat())

    @property
    def name(self) -> str:
        return self.__name

    @property
    def api_token(self) -> str:
        return self.__api_token

    @property
    def identifier(self) -> int:
        return self.__identifier

    @property
    def last_updated(self) -> datetime:
        return self.__last_updated
