from __future__ import annotations
from datetime import datetime
from tzlocal import get_localzone
from typing import Optional

from togglcmder.toggl.types.user import User


class UserBuilder(object):
    def __init__(self, user: Optional[User] = None):
        if user is not None:
            self.__identifier = user.identifier
            self.__name = user.name
            self.__api_token = user.api_token
            self.__last_updated = user.last_updated
        else:
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

    def last_updated(self, *, last_update: Optional[str] = None,
                     epoch: Optional[int] = None) -> UserBuilder:
        if last_update:
            self.__last_updated = self.__datetime_from_str(last_update)
        elif epoch:
            self.__last_updated = self.__datetime_from_timestamp(epoch)
        return self

    def build(self) -> User:
        return User(
            identifier=self.__identifier,
            name=self.__name,
            api_token=self.__api_token,
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
