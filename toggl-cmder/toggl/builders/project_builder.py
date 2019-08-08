
from toggl import project

class ProjectBuilder(object):

    @staticmethod
    def from_name_and_workspace(name, workspace):
        return project.Project(
            name=name,
            workspace_id=workspace.id
        )
