from typing import List, Tuple

from togglcmder.toggl.types.tag import Tag as TagType
from togglcmder.toggl.types.workspace import Workspace as WorkspaceType


class Tag(object):
    """
    A composition of the data we want to show in a view
    of a given tag.
    """

    def __init__(self, tags: List[TagType], workspace: WorkspaceType):
        self.__tags = tags
        self.__workspace = workspace

    @staticmethod
    def headers() -> Tuple:
        return (
            "Tag Identifier",
            "Tag Name",
            "Workspace Name"
        )

    def values(self) -> List[Tuple]:
        return [(
            tag.identifier,
            tag.name,
            self.__workspace.name,
        ) for tag in self.__tags]
