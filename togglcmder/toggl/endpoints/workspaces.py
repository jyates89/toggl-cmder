"""

"""


class Workspaces(object):
    """

    """

    def __init__(self, url: str):
        """

        :param url:
        """
        self.__url = url + "/workspaces"

    def __repr__(self):
        return self.__url

    def details(self, id_: int) -> str:
        """

        :param id_:
        :return:
        """
        return self.__url + "/{}".format(id_)

    def projects(self, id_: int) -> str:
        return self.__url + "/{}/projects".format(id_)

    def tags(self, id_: int) -> str:
        return self.__url + "/{}/tags".format(id_)
