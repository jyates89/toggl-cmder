from json import JSONDecoder

from toggl import user

class UserResponseDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        JSONDecoder.__init__(self,
                             object_hook=self.object_hook,
                             *args,
                             **kwargs)

    def object_hook(self, obj):
        return user.User(
            since=obj['since'],
            name=obj['data']['fullname'],
            id=obj['data']['id'],
        )
