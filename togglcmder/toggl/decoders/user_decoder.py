from json import JSONDecoder

from toggl.builders.user_builder import UserBuilder


class UserDecoder(JSONDecoder):
    def __init__(self, *args: tuple, **kwargs: dict):
        JSONDecoder.__init__(self,
                             object_hook=UserDecoder.object_hook,
                             *args,
                             **kwargs)

    @staticmethod
    def object_hook(obj: dict):
        if 'data' in obj:
            return obj['data']

        if 'fullname' in obj:
            return UserBuilder()\
                .identifier(obj['id'])\
                .name(obj['fullname'])\
                .api_token(obj['api_token'])\
                .last_updated(obj['at'])\
                .build()

        return obj
