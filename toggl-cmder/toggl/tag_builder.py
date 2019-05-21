from toggl import tag

class TagBuilder(object):

    @staticmethod
    def from_name(tag_name):
        return tag.Tag(
            id=None,
            name=tag_name,
            workspace_id=None)
