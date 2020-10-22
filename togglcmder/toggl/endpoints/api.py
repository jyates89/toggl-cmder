from togglcmder.toggl.endpoints.time_entries import TimeEntries
from togglcmder.toggl.endpoints.projects import Projects
from togglcmder.toggl.endpoints.tags import Tags
from togglcmder.toggl.endpoints.workspaces import Workspaces
from togglcmder.toggl.endpoints.users import Users


class API(object):
    def __init__(self, version: int = 8):
        self.__version = version
        self.__url = "https://api.track.toggl.com/api/v{}".format(
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
