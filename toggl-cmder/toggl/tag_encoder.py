from json import JSONEncoder

from toggl import tag

class TagEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, tag.Tag):
            return { 'tag' :
                         {
                             'name': o.name,
                             'wid': o.workspace_id
                         }}
        return super(TagEncoder, self).default(o)
