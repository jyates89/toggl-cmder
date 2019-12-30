"""

"""


class Users(object):
    """

    """

    def __init__(self, url: str):
        """

        :param url:
        """
        self.__url = url

    def __repr__(self):
        return self.__url + "/me"

    def details(self, extra_data: bool = False) -> str:
        if extra_data:
            return self.__url + "/me?with_related_data=true"
        return self.__url + "/me"

    def reset_api_token(self):
        return self.__url + "/reset_token"
