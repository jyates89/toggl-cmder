from json import JSONDecoder

from togglcmder.toggl.builders.project_builder import ProjectBuilder


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
                .color(int(obj['color']))\
                .last_updated(last_update=obj['at'])\
                .created(created=obj.get('created_at', None))\
                .build()

        return obj
