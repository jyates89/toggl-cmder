from toggl.types.workspace import Workspace
from toggl.types.project import Project
from toggl.types.tag import Tag
from toggl.types.time_entry import TimeEntry

class Commands(object):
    def __init__(self, *args, **kwargs):
        pass

    def add_tag(self, tag: Tag, workspace: Workspace):
        pass

    def delete_tag(self, tag: Tag, workspace: Workspace):
        pass

    def add_project(self, project: Project, workspace: Workspace):
        pass

    def delete_project(self, project: Project, workspace: Workspace):
        pass

    def add_time_entry(self, time_entry: TimeEntry, workspace: Workspace):
        pass

    def delete_time_entry(self, time_entry: TimeEntry, workspace: Workspace):
        pass
