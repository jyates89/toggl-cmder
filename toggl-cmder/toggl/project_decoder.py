from json import JSONDecoder

from toggl import project

class ProjectResponseDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        JSONDecoder.__init__(self,
                             object_hook=self.object_hook,
                             *args,
                             **kwargs)

    def object_hook(self, obj):
        print(obj)
        return project.Project(
            name=obj['name'],
            workspace_id=obj['wid'],
            project_id=['id'],
            color=obj['color']
        )
