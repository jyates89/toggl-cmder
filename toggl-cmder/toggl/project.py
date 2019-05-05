from json import JSONEncoder,JSONDecoder

class Project(object):
    def __init__(self, **kwargs):
        self.__name = kwargs.get('name')
        self.__workspace_id = kwargs.get('workspace_id')
        self.__project_id = kwargs.get('project_id')
        self.__color = kwargs.get('color', 0)

        self.__workspace_ref = kwargs.get('workspace', None)

    @property
    def name(self):
        return self.__name

    @property
    def workspace_id(self):
        return self.__workspace_id

    @property
    def project_id(self):
        return self.__project_id

    @property
    def color(self):
        return self.__color

    @property
    def workspace(self):
        return self.__workspace_ref
