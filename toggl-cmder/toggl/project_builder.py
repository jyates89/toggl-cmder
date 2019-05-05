
from toggl import project

class ProjectBuilder(object):
    def __init__(self):
        self.__workspaces = [None]
        self.__projects = [None]

    def get_new(self, workspace, name):
        return project.Project()

    def get_existing(self):
        return project.Project()
