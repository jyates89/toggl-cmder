from typing import List, Tuple

from datetime import datetime, timedelta

from togglcmder.toggl.types.time_entry import TimeEntry as TimeEntryType
from togglcmder.toggl.types.workspace import Workspace as WorkspaceType
from togglcmder.toggl.types.project import Project as ProjectType


class TimeEntry(object):
    """
    A composition of the data we want to show in a view
    of a given time entry.
    """

    def __init__(self,
                 time_entries: List[TimeEntryType],
                 project: ProjectType,
                 workspace: WorkspaceType):
        self.__time_entries = time_entries
        self.__project = project
        self.__workspace = workspace

    @staticmethod
    def headers() -> Tuple:
        return (
            "Description",
            "Project Name",
            "Workspace Name",
            # "Start Time",
            # "Stop Time",
            "Duration",
            "Tags",
            "Last Updated"
        )

    def values(self) -> List[Tuple]:
        return [(
            time_entry.description,
            self.__project.name if self.__project else "",
            self.__workspace.name,
            # time_entry.start_time.isoformat(),
            # time_entry.stop_time.isoformat() if time_entry.stop_time else "",
            str(timedelta(seconds=time_entry.duration if time_entry.duration > 0 else
                time_entry.start_time.timestamp() - datetime.now().timestamp())),
            ",".join(tag for tag in time_entry.tags) if time_entry.tags else "",
            time_entry.last_updated.isoformat(),
        ) for time_entry in self.__time_entries]

    def values_sorted(self) -> List[Tuple]:
        return sorted(self.values(),
                      key=lambda entry: entry[3])
