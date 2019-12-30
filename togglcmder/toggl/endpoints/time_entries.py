"""

"""
from datetime import datetime
from typing import List, Optional

import urllib.parse


class TimeEntries(object):
    """

    """

    def __init__(self, url: str):
        self.__url = url + "/time_entries"

    def __repr__(self):
        return self.__url

    def start(self) -> str:
        """
        Used to start a new entry, with details in a POST request.

        :return:
        """
        return self.__url + "/start"

    def stop(self, id_: int) -> str:
        """
        Used to stop a specific entry.

        :param id_:
        :return:
        """
        return self.__url + "/{}/stop".format(id_)

    def current(self) -> str:
        """
        Only used to return the current running entry.

        :return:
        """
        return self.__url + "/current"

    def details(self, identifier: Optional[int] = None, identifiers: Optional[List[int]] = None) -> str:
        """
        This can be used for multiple types of requests, such as:
            1. Simply getting more details on the entry.
            2. Updating the entry.
            3. Deleting the entry.
            4. Handling more than one time entry.

        :param identifier:
        :param identifiers:
        :return:
        """
        if identifier:
            return self.__url + "/{}".format(identifier)
        elif identifiers:
            return self.__url + "/{}".format(",".join(map(str, identifiers)))
        else:
            return self.__url

    # Used to search for time entries with a GET request.
    def search(self, start: datetime, end: datetime) -> str:
        return self.__url + "?start_date={}&end_date={}".format(
            urllib.parse.quote(start.isoformat()),
            urllib.parse.quote(end.isoformat()))
