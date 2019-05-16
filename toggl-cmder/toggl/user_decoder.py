import json
from json import JSONDecoder

from toggl import user

from toggl import tag_decoder
from toggl import workspace_decoder
from toggl import project_decoder
from toggl import time_entry_decoder

class UserDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        JSONDecoder.__init__(self,
                             object_hook=self.object_hook,
                             *args,
                             **kwargs)

    def object_hook(self, obj):
        # for some reason, the data passed in here isn't consistent
        # so we need to check for the data attribute
        print(obj)
        if not obj.get('data', None):
            return
        return user.User(
            full_name=obj['data']['fullname'],
            id=obj['data']['id'],
            tags=json.loads(obj['data']['tags'],
                            cls=tag_decoder.TagDecoder),
            workspaces=json.loads(obj['data']['workspace'],
                                  cls=workspace_decoder.WorkspaceDecoder),
            projects=json.loads(obj['data']['projects'],
                                cls=project_decoder.ProjectDecoder),
            time_entries=json.loads(obj['data']['time_entries'],
                                    cls=time_entry_decoder.TimeEntryDecoder)
        )
