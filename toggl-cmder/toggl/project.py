
from datetime import datetime

class Project(object):
    def __init__(self, **kwargs):
        self.__name = kwargs.get('name')
        self.__workspace_id = kwargs.get('workspace_id')
        self.__id = kwargs.get('project_id', 0)
        self.__color = kwargs.get('color', 0)
        self.__hex_color = kwargs.get('hex_color', 0)

        # strptime returns a tuple, so we unpack it here
        if kwargs.get('created', None) is not None:
            self.__created, = datetime.strptime(
                kwargs.get('created'),
                '%Y-%m-%dT%H:%M:%S%z'),

        self.__workspace_ref = None # workspace.workspace

    @property
    def name(self):
        return self.__name

    @property
    def workspace_id(self):
        return self.__workspace_id

    @property
    def id(self):
        return self.__id

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

    @staticmethod
    def api_url():
        return "https://www.toggl.com/api/v8/projects"

    @staticmethod
    def api_multi_project_url(id_list):
        if not isinstance(id_list, list):
            raise TypeError("id_list must be of type 'list'")

        return Project.api_url() + "/{}".format(
            # map any non-string to string in list
            ",".join(map(str, id_list))
        )

    def api_project_details_url(self):
        return Project.api_url() + "/{}".format(
            self.__id
        )
