import json
import os

class UserCache(object):
    def __init__(self):
        self.__file_name = "toggl_cache.json"

        self.__data = {}

    def update_cache(self, data):
        if not isinstance(data, dict):
            raise ValueError("dict required")
        if data == self.__data:
            return
        self.__data = data
        file = open(self.__file_name, 'w')
        file.write(json.dumps(data, indent=4))
        file.close()

    def read_cache(self):
        file = open(self.__file_name, 'r')
        self.__data = file.read()
        file.close()
        return json.load(self.__data)

    def clear_cache(self):
        os.remove(self.__file_name)

    @property
    def file_name(self):
        return self.__file_name

    @property
    def data(self):
        return self.__data
