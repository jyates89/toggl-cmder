from datetime import datetime

from typing import List, Optional


class TimeEntry(object):
    def __init__(self, *, description: str, start_time: datetime,
                 identifier: Optional[int] = None,
                 project_identifier: Optional[int] = None,
                 workspace_identifier: Optional[int] = None,
                 stop_time: Optional[datetime] = None,
                 duration: Optional[int] = None,
                 tags: Optional[List[str]] = None,
                 last_updated: Optional[datetime] = None):
        self.__description = description
        self.__start_time = start_time
        self.__identifier = identifier
        self.__project_identifier = project_identifier
        self.__workspace_identifier = workspace_identifier
        self.__stop_time = stop_time
        self.__duration = duration
        self.__tags = tags
        self.__last_updated = last_updated

    def __eq__(self, other):
        if not isinstance(other, TimeEntry):
            return NotImplemented

        return self.__description == other.description \
            and self.__start_time == other.start_time \
            and self.__identifier == other.identifier \
            and self.__project_identifier == other.project_identifier \
            and self.__workspace_identifier == other.workspace_identifier \
            and self.__stop_time == other.stop_time \
            and self.__duration == other.duration \
            and self.__tags == other.tags \
            and self.__last_updated == other.last_updated

    def __str__(self):
        return """
            description = {},
            start_time = {},
            stop_time = {},
            duration = {},
            identifier = {},
            project_identifier = {},
            workspace_identifier = {},
            tags = {},
            last_updated = {}
        """.format(
            self.description,
            self.start_time.isoformat(),
            self.stop_time.isoformat(),
            self.duration,
            self.identifier,
            self.project_identifier,
            self.workspace_identifier,
            self.tags,
            self.last_updated
        )
    @property
    def description(self) -> str:
        return self.__description

    @property
    def start_time(self) -> datetime:
        return self.__start_time

    @property
    def identifier(self) -> int:
        return self.__identifier

    @property
    def project_identifier(self) -> int:
        return self.__project_identifier

    @property
    def workspace_identifier(self) -> int:
        return self.__workspace_identifier

    @property
    def stop_time(self) -> datetime:
        return self.__stop_time

    @property
    def duration(self) -> int:
        return self.__duration

    @property
    def tags(self) -> List[str]:
        return self.__tags

    @property
    def last_updated(self) -> datetime:
        return self.__last_updated
