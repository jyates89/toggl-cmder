from typing import List, Tuple

from togglcmder.toggl.types.project import Project as ProjectType
from togglcmder.toggl.types.workspace import Workspace as WorkspaceType


class Project(object):
    """
    A composition of the data we want to show in a view
    of a given project.
    """

    def __init__(self, *, projects: List[ProjectType], workspace: WorkspaceType):
        self.__projects = projects
        self.__workspace = workspace

    @staticmethod
    def headers() -> Tuple:
        return (
            "Project Identifier",
            "Project Name",
            "Workspace Name",
            "Color Designation",
            "Last Updated"
        )

    def values(self) -> List[Tuple]:
        return [(
            project.identifier,
            project.name,
            self.__workspace.name,
            project.color,
            project.last_updated.isoformat()
        ) for project in self.__projects]
