"""

"""
from typing import List, Optional


class Projects(object):
    """
    """

    def __init__(self, url: str):
        """

        :param url:
        """
        self.__url = url + "/projects"

    def __repr__(self):
        return self.__url

    def details(self, identifier: Optional[int] = None, identifiers: Optional[List[int]] = None) -> str:
        """

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
