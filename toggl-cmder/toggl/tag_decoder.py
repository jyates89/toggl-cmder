from json import JSONDecoder

from toggl import tag

class TagResponseDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        JSONDecoder.__init__(self,
                             object_hook=self.object_hook,
                             *args,
                             **kwargs)

    def object_hook(self, obj):
        return tag.Tag(
            id=obj['id'],
            name=obj['name'],
            workspace_id=obj['wid'],
            created=obj['at']
        )
