from json import JSONDecoder

from toggl import workspace

class WorkspaceDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        JSONDecoder.__init__(self,
                             object_hook=self.object_hook,
                             *args,
                             **kwargs)

    def object_hook(self, obj):
        return workspace.Workspace(
            id=obj['id'],
            name=obj['name']
        )
