

class Tag(object):
    def __init__(self, **kwargs):
        super(Tag, self).__init__(kwargs)
        self.__name = kwargs.get('name', None)
        self.__workspace_id = kwargs.get('workspace_id', None)

        self.__workspace_ref = kwargs.get('workspace', None)

    @property
    def name(self):
        return self.__name

    @property
    def workspace_id(self):
        return self.__workspace_id

    @property
    def workspace(self):
        return self.__workspace_ref
