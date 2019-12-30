from toggl.endpoints.time_entries import TimeEntries
from toggl.endpoints.projects import Projects
from toggl.endpoints.tags import Tags
from toggl.endpoints.workspaces import Workspaces
from toggl.endpoints.users import Users


class API(object):
    def __init__(self, version: int = 8):
        self.__version = version
        self.__url = "https://www.toggl.com/api/v{}".format(
            self.__version
        )

    @property
    def time_entries(self) -> TimeEntries:
        return TimeEntries(url=self.__url)

    @property
    def projects(self) -> Projects:
        return Projects(url=self.__url)

    @property
    def tags(self) -> Tags:
        return Tags(url=self.__url)

    @property
    def workspaces(self) -> Workspaces:
        return Workspaces(url=self.__url)

    @property
    def users(self) -> Users:
        return Users(url=self.__url)
