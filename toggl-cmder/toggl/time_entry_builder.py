
from datetime import datetime,timezone

from toggl import time_entry
from toggl import tag_builder

class TimeEntryBuilder(object):
    @staticmethod
    def from_now(workspace, project, description, tags=None):
        built_tags = [tag_builder.TagBuilder.from_name(tag) for tag in tags]
        return time_entry.TimeEntry(
            id=None,
            wid=workspace.id,
            pid=project.id,
            description=description,
            start=datetime.now(timezone.utc).isoformat(),
            tags=built_tags)

    @staticmethod
    def from_start(start, workspace_id, project_id):
        pass
