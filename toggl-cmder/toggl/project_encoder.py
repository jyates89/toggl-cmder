from json import JSONEncoder

from toggl import project

class ProjectEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, project.Project):
            return { 'project' : o.__dict__}
        return super(ProjectEncoder, self).default(o)
