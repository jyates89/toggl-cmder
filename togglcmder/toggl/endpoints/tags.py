"""

"""


class Tags(object):
    """

    """

    def __init__(self, url: str):
        """

        :param url:
        """
        self.__url = url + "/tags"

    def __repr__(self):
        return self.__url

    def details(self, identifier: int) -> str:
        """

        :param identifier:
        :return:
        """
        return self.__url + "/{}".format(identifier)
