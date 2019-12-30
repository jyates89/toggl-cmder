import unittest
import json

from datetime import datetime
from pytz import timezone

from toggl.types.project import Project
from toggl.decoders.project_decoder import ProjectDecoder

from toggl.types.tag import Tag
from toggl.decoders.tag_decoder import TagDecoder

from toggl.types.time_entry import TimeEntry
from toggl.decoders.time_entry_decoder import TimeEntryDecoder

from toggl.types.user import User
from toggl.decoders.user_decoder import UserDecoder

from toggl.types.workspace import Workspace
from toggl.decoders.workspace_decoder import WorkspaceDecoder


class TestDecoders(unittest.TestCase):
    def test_project_decoding(self):
        # Sample data taken from Toggl API reference on Github.
        json_data = {
            "data": {
                "id": 193838628,
                "wid": 777,
                "cid": 123397,
                "name": "An awesome project",
                "billable": False,
                "is_private": True,
                "active": True,
                "at": "2013-03-06T12:15:37+00:00",
                "template": True,
                "color": 5
            }
        }
        project = json.loads(json.dumps(json_data), cls=ProjectDecoder)

        self.assertIsInstance(project, Project)

        self.assertEqual(project.name, json_data['data']['name'])
        self.assertEqual(project.workspace_identifier, json_data['data']['wid'])
        self.assertEqual(project.identifier, json_data['data']['id'])
        self.assertEqual(project.last_updated.isoformat(), json_data['data']['at'])
        self.assertEqual(project.color, Project.Color(5))

    def test_tag_decoding(self):
        # Sample data taken from Toggl API reference on Github.
        json_data = {
            "data": {
                "id": 1239455,
                "wid": 777,
                "name": "not billed"
            }
        }
        tag = json.loads(json.dumps(json_data), cls=TagDecoder)

        self.assertIsInstance(tag, Tag)

        self.assertEqual(tag.name, json_data['data']['name'])
        self.assertEqual(tag.workspace_identifier, json_data['data']['wid'])
        self.assertEqual(tag.identifier, json_data['data']['id'])

    def test_time_entry_created_decoding(self):
        # Sample data taken from Toggl API reference on Github.
        json_data = {
            "data": {
                "id": 436694100,
                "pid": 123,
                "wid": 777,
                "billable": False,
                "start": "2013-03-05T07:58:58.000Z",
                "duration": 1200,
                "description": "Meeting with possible clients",
                "tags": [
                    "billed"
                ]
            }
        }

        time_entry = json.loads(json.dumps(json_data), cls=TimeEntryDecoder)

        self.assertIsInstance(time_entry, TimeEntry)

        self.assertEqual(time_entry.start_time,
                         datetime.strptime(json_data['data']['start'], '%Y-%m-%dT%H:%M:%S.%fZ').replace(
                             tzinfo=timezone('UTC')))
        self.assertEqual(time_entry.identifier, json_data['data']['id'])
        self.assertEqual(time_entry.project_identifier, json_data['data']['pid'])
        self.assertEqual(time_entry.workspace_identifier, json_data['data']['wid'])
        self.assertEqual(time_entry.duration, json_data['data']['duration'])
        self.assertEqual(time_entry.description, json_data['data']['description'])
        self.assertEqual(time_entry.tags, json_data['data']['tags'])

    def test_time_entry_detail_decoding(self):
        # Sample data taken from Toggl API reference on Github.
        json_data = {
            "data": {
                "id": 436694100,
                "wid": 777,
                "pid": 193791,
                "tid": 13350500,
                "billable": False,
                "start": "2013-02-27T01:24:00+00:00",
                "stop": "2013-02-27T07:24:00+00:00",
                "duration": 21600,
                "description": "Some serious work",
                "tags": [
                    "billed"
                ],
                "at": "2013-02-27T13:49:18+00:00"
            }
        }

        time_entry = json.loads(json.dumps(json_data), cls=TimeEntryDecoder)

        self.assertIsInstance(time_entry, TimeEntry)

        self.assertEqual(time_entry.start_time.isoformat(), json_data['data']['start'])
        self.assertEqual(time_entry.stop_time.isoformat(), json_data['data']['stop'])
        self.assertEqual(time_entry.identifier, json_data['data']['id'])
        self.assertEqual(time_entry.project_identifier, json_data['data']['pid'])
        self.assertEqual(time_entry.workspace_identifier, json_data['data']['wid'])
        self.assertEqual(time_entry.duration, json_data['data']['duration'])
        self.assertEqual(time_entry.description, json_data['data']['description'])
        self.assertEqual(time_entry.tags, json_data['data']['tags'])
        self.assertEqual(time_entry.last_updated.isoformat(), json_data['data']['at'])

    def test_time_entry_started_decoding(self):
        # Sample data taken from Toggl API reference on Github.
        json_data = {
            "data": {
                "id": 436694100,
                "pid": 123,
                "wid": 777,
                "billable": False,
                "start": "2013-03-05T07:58:58.000Z",
                "duration": -1362470338,
                "description": "Meeting with possible clients",
                "tags": [
                    "billed"
                ]
            }
        }
        time_entry = json.loads(json.dumps(json_data), cls=TimeEntryDecoder)

        self.assertIsInstance(time_entry, TimeEntry)
        self.assertEqual(time_entry.start_time,
                         datetime.strptime(json_data['data']['start'], '%Y-%m-%dT%H:%M:%S.%fZ').replace(
                             tzinfo=timezone('UTC')))
        self.assertEqual(time_entry.identifier, json_data['data']['id'])
        self.assertEqual(time_entry.project_identifier, json_data['data']['pid'])
        self.assertEqual(time_entry.workspace_identifier, json_data['data']['wid'])

        duration = datetime.now(timezone('UTC')).replace(microsecond=0).timestamp() + json_data['data']['duration']
        self.assertEqual(time_entry.duration, duration)

        self.assertEqual(time_entry.description, json_data['data']['description'])
        self.assertEqual(time_entry.tags, json_data['data']['tags'])

    def test_time_entry_stopped_decoding(self):
        # Sample data taken from Toggl API reference on Github.
        json_data = {
            "data": {
                "id": 436694100,
                "pid": 123,
                "wid": 777,
                "billable": False,
                "start": "2013-03-05T07:58:58.000Z",
                "duration": 60,
                "description": "Meeting with possible clients",
                "tags": [
                    "billed"
                ]
            }
        }

        time_entry = json.loads(json.dumps(json_data), cls=TimeEntryDecoder)

        self.assertIsInstance(time_entry, TimeEntry)
        self.assertEqual(time_entry.start_time,
                         datetime.strptime(json_data['data']['start'], '%Y-%m-%dT%H:%M:%S.%fZ').replace(
                             tzinfo=timezone('UTC')))
        self.assertEqual(time_entry.identifier, json_data['data']['id'])
        self.assertEqual(time_entry.project_identifier, json_data['data']['pid'])
        self.assertEqual(time_entry.workspace_identifier, json_data['data']['wid'])
        self.assertEqual(time_entry.duration, json_data['data']['duration'])
        self.assertEqual(time_entry.description, json_data['data']['description'])
        self.assertEqual(time_entry.tags, json_data['data']['tags'])

    def test_time_entry_search_decoding(self):
        # Sample data taken from Toggl API reference on Github.
        json_data = {"data": [
            {
                "id": 436691234,
                "wid": 777,
                "pid": 123,
                "billable": True,
                "start": "2013-03-11T11:36:00+00:00",
                "stop": "2013-03-11T15:36:00+00:00",
                "duration": 14400,
                "description": "Meeting with the client",
                "tags": [""],
                "at": "2013-03-11T15:36:58+00:00"
            }, {
                "id": 436776436,
                "wid": 777,
                "billable": False,
                "start": "2013-03-12T10:32:43+00:00",
                "stop": "2013-03-12T14:32:43+00:00",
                "duration": 18400,
                "description": "important work",
                "tags": [""],
                "at": "2013-03-12T14:32:43+00:00"
            }
        ]}

        time_entries = json.loads(json.dumps(json_data), cls=TimeEntryDecoder)

        for entry in time_entries:
            self.assertIsInstance(entry, TimeEntry)

    def test_user_decoding(self):
        # Sample data taken from Toggl API reference on Github.
        json_data = {
            "since": 1362575771,
            "data": {
                "id": 9000,
                "api_token": "1971800d4d82861d8f2c1651fea4d212",
                "default_wid": 777,
                "email": "johnt@swift.com",
                "fullname": "John Swift",
                "jquery_timeofday_format": "h:i A",
                "jquery_date_format": "m/d/Y",
                "timeofday_format": "h:mm A",
                "date_format": "MM/DD/YYYY",
                "store_start_and_stop_time": True,
                "beginning_of_week": 0,
                "language": "en_US",
                "image_url": "https://www.toggl.com/system/avatars/9000/small/open-uri20121116-2767-b1qr8l.png",
                "sidebar_piechart": False,
                "at": "2013-03-06T12:18:42+00:00",
                "retention": 9,
                "record_timeline": True,
                "render_timeline": True,
                "timeline_enabled": True,
                "timeline_experiment": True,
                "new_blog_post": {},
                "invitation": {}
            }
        }

        user_data = json.loads(json.dumps(json_data), cls=UserDecoder)

        self.assertIsInstance(user_data, User)

        self.assertEqual(user_data.identifier, json_data['data']['id'])
        self.assertEqual(user_data.last_updated.isoformat(), json_data['data']['at'])
        self.assertEqual(user_data.name, json_data['data']['fullname'])
        self.assertEqual(user_data.api_token, json_data['data']['api_token'])

    def test_workspace_decoding(self):
        json_data = {"data": [
            {
                "id": 3134975,
                "name": "John's personal ws",
                "premium": True,
                "admin": True,
                "default_hourly_rate": 50,
                "default_currency": "USD",
                "only_admins_may_create_projects": False,
                "only_admins_see_billable_rates": True,
                "rounding": 1,
                "rounding_minutes": 15,
                "at": "2013-08-28T16:22:21+00:00",
                "logo_url": "my_logo.png"
            }, {
                "id": 777,
                "name": "My Company Inc",
                "premium": True,
                "admin": True,
                "default_hourly_rate": 40,
                "default_currency": "EUR",
                "only_admins_may_create_projects": False,
                "only_admins_see_billable_rates": True,
                "rounding": 1,
                "rounding_minutes": 15,
                "at": "2013-08-28T16:22:21+00:00"
            }
        ]}

        workspaces = json.loads(json.dumps(json_data), cls=WorkspaceDecoder)

        workspace_index = 0

        for workspace in workspaces:
            self.assertIsInstance(workspace, Workspace)

            self.assertEqual(workspace.name, json_data['data'][workspace_index]['name'])
            self.assertEqual(workspace.identifier, json_data['data'][workspace_index]['id'])
            self.assertEqual(workspace.last_updated.isoformat(), json_data['data'][workspace_index]['at'])

            workspace_index += 1
