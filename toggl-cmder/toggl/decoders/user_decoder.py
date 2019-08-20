import json
from json import JSONDecoder

from toggl import user

from toggl.decoders import tag_decoder
from toggl.decoders import workspace_decoder
from toggl.decoders import project_decoder
from toggl.decoders import time_entry_decoder

class UserDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        JSONDecoder.__init__(self,
                             object_hook=self.object_hook,
                             *args,
                             **kwargs)

    def object_hook(self, obj):
        if not 'data' in obj:
            return obj

        return user.User(
            full_name=obj['data'].get('fullname'),
            id=obj['data'].get('id'),
            api_token=obj['data'].get('api_token'),
            timestamp=obj['data'].get('at'),
            tags=json.loads(json.dumps(obj['data'].get('tags')),
                            cls=tag_decoder.TagDecoder),
            workspaces=json.loads(json.dumps(obj['data'].get('workspaces')),
                                  cls=workspace_decoder.WorkspaceDecoder),
            projects=json.loads(json.dumps(obj['data'].get('projects')),
                                cls=project_decoder.ProjectDecoder),
            time_entries=json.loads(json.dumps(obj['data'].get('time_entries')),
                                    cls=time_entry_decoder.TimeEntryDecoder)
        )
