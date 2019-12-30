from __future__ import annotations
from datetime import datetime
from pytz import timezone

from toggl.types.user import User


class UserBuilder(object):
    def __init__(self):
        self.__identifier = None
        self.__name = None
        self.__api_token = None
        self.__last_updated = None

    def identifier(self, identifier: int) -> UserBuilder:
        self.__identifier = identifier
        return self

    def name(self, name: str) -> UserBuilder:
        self.__name = name
        return self

    def api_token(self, api_token: str) -> UserBuilder:
        self.__api_token = api_token
        return self

    def last_updated(self, last_update: str) -> UserBuilder:
        if last_update is not None:
            try:
                self.__last_updated = datetime.strptime(last_update, '%Y-%m-%dT%H:%M:%S%z')
            except ValueError:
                # try and see if timezone if UTC
                self.__last_updated = datetime.strptime(last_update, '%Y-%m-%dT%H:%M:%S.%fZ')\
                    .replace(tzinfo=timezone('UTC'))
        return self

    def build(self) -> User:
        return User(
            identifier=self.__identifier,
            name=self.__name,
            api_token=self.__api_token,
            last_updated=self.__last_updated)
