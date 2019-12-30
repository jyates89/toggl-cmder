from json import JSONDecoder

from toggl.builders.project_builder import ProjectBuilder
from toggl.types.project import Project


class ProjectDecoder(JSONDecoder):
    def __init__(self, *args: tuple, **kwargs: dict):
        JSONDecoder.__init__(self,
                             object_hook=ProjectDecoder.object_hook,
                             *args,
                             **kwargs)

    @staticmethod
    def object_hook(obj: dict):
        if 'data' in obj:
            return obj['data']

        if 'id' in obj:
            return ProjectBuilder()\
                .identifier(obj['id'])\
                .name(obj['name'])\
                .workspace_identifier(obj['wid'])\
                .color(obj['color'])\
                .last_updated(obj['at'])\
                .created(obj.get('created_at', None))\
                .build()

        return obj
