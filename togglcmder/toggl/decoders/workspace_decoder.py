from json import JSONDecoder

from toggl.builders.workspace_builder import WorkspaceBuilder


class WorkspaceDecoder(JSONDecoder):
    def __init__(self, *args: tuple, **kwargs: dict):
        JSONDecoder.__init__(self,
                             object_hook=self.object_hook,
                             *args,
                             **kwargs)

    @staticmethod
    def object_hook(obj: dict):
        if 'data' in obj:
            return obj['data']

        if 'id' in obj:
            return WorkspaceBuilder()\
                .identifier(obj['id'])\
                .name(obj['name'])\
                .last_updated(obj['at'])\
                .build()

        return obj
