from json import JSONEncoder

from toggl import project

class ProjectEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, project.Project):
            return { 'project' :
                         {
                             'name': o.name,
                             'wid': o.workspace_id
                         }}
        return super(ProjectEncoder, self).default(o)
