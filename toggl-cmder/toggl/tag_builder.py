from toggl import tag

"""

"""
class TagBuilder(object):

    def __init__(self):
        pass

    """
    Create a new tag in a given workspace.
    """
    def create_new(self):
        return tag.Tag()

    """
    Get existing tags in a given workspace.
    """
    def get_existing(self, workspace):
        return tag.Tag()
