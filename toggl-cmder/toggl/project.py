
from datetime import datetime

class Project(object):
    API_URL = ""
    def __init__(self, **kwargs):
        self.__name = kwargs.get('name')
        self.__workspace_id = kwargs.get('workspace_id')
        self.__project_id = kwargs.get('project_id')
        self.__color = kwargs.get('color', 0)
        self.__hex_color = kwargs.get('hex_color', 0)
        # strptime returns a tuple, so we unpack it here
        self.__created, = datetime.strptime(kwargs.get('created'), '%Y-%m-%dT%H:%M:%S%z'),

        self.__workspace_ref = None # workspace.workspace

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
    def hex_color(self):
        return self.__hex_color

    @property
    def created(self):
        return self.__created

    @property
    def workspace(self):
        return self.__workspace_ref

    @workspace.setter
    def workspace(self, workspace):
        self.__workspace_ref = workspace
