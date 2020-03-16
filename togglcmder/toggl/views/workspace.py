from typing import List, Tuple

from togglcmder.toggl.types.workspace import Workspace as WorkspaceType


class Workspace(object):
    """
    A composition of the data we want to show in a view
    of a given workspace.
    """

    def __init__(self, workspaces: List[WorkspaceType]):
        self.__workspaces = workspaces

    @staticmethod
    def headers() -> Tuple:
        return (
            "Identifier",
            "Workspace Name",
            "Last Updated"
        )

    def values(self) -> List[Tuple]:
        return [(
            workspace.identifier,
            workspace.name,
            workspace.last_updated.isoformat()
        ) for workspace in self.__workspaces]
