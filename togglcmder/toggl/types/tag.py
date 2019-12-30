from typing import Optional


class Tag(object):
    def __init__(self, *, name: str, workspace_identifier: int,
                 identifier: Optional[int] = None):
        self.__name = name
        self.__workspace_identifier = workspace_identifier
        self.__identifier = identifier

    def __eq__(self, other):
        if not isinstance(other, Tag):
            return NotImplemented

        return self.__name == other.name \
            and self.__workspace_identifier == other.workspace_identifier \
            and self.__identifier == other.identifier

    def __str__(self):
        return """
            tag name = {},
            tag identifier = {},
            tag workspace identifier = {}
        """.format(
            self.name,
            self.identifier,
            self.workspace_identifier
        )
    @property
    def name(self) -> str:
        return self.__name

    @property
    def identifier(self) -> int:
        return self.__identifier

    @property
    def workspace_identifier(self) -> int:
        return self.__workspace_identifier
