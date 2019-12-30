from json import JSONEncoder

from toggl.types.project import Project


class ProjectEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Project):
            project = {'project': {
                'name': obj.name,
                'wid': obj.workspace_identifier,
            }}
            if obj.color is not None:
                project['project']['color'] = obj.color.value
            return project
        return super(ProjectEncoder, self).default(obj)
