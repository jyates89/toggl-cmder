from datetime import datetime

class Tag(object):
    def __init__(self, **kwargs):
        self.__id = kwargs.get('id')
        self.__name = kwargs.get('name')
        self.__workspace_id = kwargs.get('workspace_id')

    @property
    def name(self):
        return self.__name

    @property
    def id(self):
        return self.__id

    @property
    def workspace_id(self):
        return self.__workspace_id

    @staticmethod
    def api_url():
        return "https://www.toggl.com/api/v8/tags"

    def api_tag_details_url(self):
        return Tag.api_url() + "/{}".format(
            self.__id
        )
