import unittest
import json
from datetime import datetime, timedelta
from pytz import timezone

from toggl.builders.time_entry_builder import TimeEntryBuilder
from toggl.builders.project_builder import ProjectBuilder
from toggl.builders.tag_builder import TagBuilder

from toggl.encoders.project_encoder import ProjectEncoder
from toggl.encoders.time_entry_encoder import TimeEntryEncoder
from toggl.encoders.tag_encoder import TagEncoder


class TestEncoders(unittest.TestCase):
    def test_project_encoding(self):
        expected_project = {
            'project': {
                'name': 'Project Name',
                'wid': 1234,
                'color': 1,
            }
        }

        project = ProjectBuilder()\
            .name(expected_project['project']['name'])\
            .workspace_identifier(expected_project['project']['wid'])\
            .color(expected_project['project']['color'])\
            .build()

        self.assertDictEqual(json.loads(json.dumps(project, cls=ProjectEncoder)),
                             expected_project)

    def test_tag_encoding(self):
        expected_tag = {
            'tag': {
                'name': 'Tag Name',
                'wid': 1234
            }
        }

        tag = TagBuilder()\
            .name(expected_tag['tag']['name'])\
            .workspace_identifier(expected_tag['tag']['wid'])\
            .build()

        self.assertDictEqual(json.loads(json.dumps(tag, cls=TagEncoder)), expected_tag)

    def testing_time_entry_encoding(self):
        current_time = datetime.now(timezone('EST')).replace(microsecond=0)
        delta_time = timedelta(hours=2)
        stop_time = current_time + delta_time
        expected_time_entry = {
            'time_entry': {
                'description': 'Some time entry.',
                'tags': [
                    'Some tag goes here.',
                    'Another tag goes here.'
                ],
                'pid': 1234,
                'start': current_time.isoformat(),
                'duration': delta_time.seconds,
                'stop': stop_time.isoformat(),
                'created_with': 'toggl_cmder'
            }
        }

        time_entry = TimeEntryBuilder()\
            .description(expected_time_entry['time_entry']['description'])\
            .project_identifier(expected_time_entry['time_entry']['pid'])\
            .start_time(current_time.isoformat())\
            .duration(delta_time.seconds)\
            .stop_time(stop_time.isoformat())\
            .tags(expected_time_entry['time_entry']['tags'])\
            .build()

        self.assertDictEqual(json.loads(json.dumps(time_entry, cls=TimeEntryEncoder)),
                             expected_time_entry)


if __name__ == '__main__':
    unittest.main()
