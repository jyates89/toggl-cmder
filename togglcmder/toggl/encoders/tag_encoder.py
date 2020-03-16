from json import JSONEncoder

from togglcmder.toggl.types.tag import Tag


class TagEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Tag):
            return {'tag': {
                'name': obj.name,
                'wid': obj.workspace_identifier
            }}
        return super(TagEncoder, self).default(obj)
