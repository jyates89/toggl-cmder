from json import JSONDecoder

from togglcmder.toggl.builders.tag_builder import TagBuilder


class TagDecoder(JSONDecoder):
    def __init__(self, *args: tuple, **kwargs: dict):
        JSONDecoder.__init__(self,
                             object_hook=TagDecoder.object_hook,
                             *args,
                             **kwargs)

    @staticmethod
    def object_hook(obj: dict):
        if 'data' in obj:
            return obj['data']

        if 'id' in obj:
            return TagBuilder()\
                .identifier(obj['id'])\
                .name(obj['name'])\
                .workspace_identifier(obj['wid'])\
                .build()

        return obj
