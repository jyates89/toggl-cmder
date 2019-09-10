
from datetime import datetime,timezone

from toggl import time_entry
from toggl.builders import tag_builder

class TimeEntryBuilder(object):
    @staticmethod
    def from_now(workspace, project, description, tags=None):
        if tags:
            built_tags = [tag_builder.TagBuilder.from_name(tag) for tag in tags]
        else:
            built_tags = []
        return time_entry.TimeEntry(
            id=None,
            wid=workspace.id if workspace else None,
            pid=project.id if project else None,
            description=description,
            start=datetime.now(timezone.utc).isoformat(),
            tag_refs=built_tags)

    @staticmethod
    def from_start(start, workspace_id, project_id):
        pass
