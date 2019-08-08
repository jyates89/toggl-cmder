from json import JSONDecoder

from toggl import project

class ProjectDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        JSONDecoder.__init__(self,
                             object_hook=self.object_hook,
                             *args,
                             **kwargs)

    def object_hook(self, obj):
        return project.Project(
            name=obj['name'],
            workspace_id=obj['wid'],
            project_id=obj['id'],
            color=obj['color'],
            hex_color=obj['hex_color'],
            created=obj['created_at']
        )
