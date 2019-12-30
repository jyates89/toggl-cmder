import unittest
import urllib.parse

from datetime import datetime
from pytz import timezone

from toggl.endpoints.api import API


class TestEndpoints(unittest.TestCase):
    ENDPOINT_URL_FORMAT = "{endpoint}/v{version}/{type}{arguments}"

    DEFAULT_ENDPOINT = "https://www.toggl.com/api"
    DEFAULT_VERSION = 8

    def test_time_entries_base(self):
        time_entry_url = API(version=TestEndpoints.DEFAULT_VERSION).time_entries.__repr__()

        expected_url = TestEndpoints.ENDPOINT_URL_FORMAT.format(
            endpoint=TestEndpoints.DEFAULT_ENDPOINT,
            version=TestEndpoints.DEFAULT_VERSION,
            type="time_entries",
            arguments=""
        )

        if time_entry_url != expected_url:
            self.fail("{} ne {}".format(expected_url, time_entry_url))

    def test_time_entries_details(self):
        time_entry_id = 1

        time_entry_url = API(version=TestEndpoints.DEFAULT_VERSION).time_entries.details(time_entry_id)

        expected_url = TestEndpoints.ENDPOINT_URL_FORMAT.format(
            endpoint=TestEndpoints.DEFAULT_ENDPOINT,
            version=TestEndpoints.DEFAULT_VERSION,
            type="time_entries",
            arguments="/{}".format(time_entry_id)
        )

        if time_entry_url != expected_url:
            self.fail("{} ne {}".format(expected_url, time_entry_url))

    def test_multiple_time_entries_details(self):
        time_entry_ids = [1, 2, 3, 4]

        time_entry_url = API(version=TestEndpoints.DEFAULT_VERSION).time_entries.details(identifiers=time_entry_ids)

        expected_url = TestEndpoints.ENDPOINT_URL_FORMAT.format(
            endpoint=TestEndpoints.DEFAULT_ENDPOINT,
            version=TestEndpoints.DEFAULT_VERSION,
            type="time_entries",
            arguments="/{}".format(",".join(map(str, time_entry_ids)))
        )

        if time_entry_url != expected_url:
            self.fail("{} ne {}".format(expected_url, time_entry_url))

    def test_time_entries_start(self):
        time_entry_url = API(version=TestEndpoints.DEFAULT_VERSION).time_entries.start()

        expected_url = TestEndpoints.ENDPOINT_URL_FORMAT.format(
            endpoint=TestEndpoints.DEFAULT_ENDPOINT,
            version=TestEndpoints.DEFAULT_VERSION,
            type="time_entries/start",
            arguments=""
        )

        if time_entry_url != expected_url:
            self.fail("{} ne {}".format(expected_url, time_entry_url))

    def test_time_entries_stop(self):
        time_entry_id = 1

        time_entry_url = API(version=TestEndpoints.DEFAULT_VERSION).time_entries.stop(time_entry_id)

        expected_url = TestEndpoints.ENDPOINT_URL_FORMAT.format(
            endpoint=TestEndpoints.DEFAULT_ENDPOINT,
            version=TestEndpoints.DEFAULT_VERSION,
            type="time_entries",
            arguments="/{}/stop".format(time_entry_id)
        )

        if time_entry_url != expected_url:
            self.fail("{} ne {}".format(expected_url, time_entry_url))

    def test_time_entries_search(self):
        # The dates used in the generated URLs"
        start_date = datetime(2019, 12, 1, 10, 0, 0, tzinfo=timezone('EST'))
        end_date = datetime(2019, 12, 1, 11, 0, 0, tzinfo=timezone('EST'))

        # The URL under test:
        time_entry_url = API(version=TestEndpoints.DEFAULT_VERSION).time_entries.search(
            start=start_date,
            end=end_date)

        # The expected result as generated here in the test case:
        expected_url = TestEndpoints.ENDPOINT_URL_FORMAT.format(
            endpoint=TestEndpoints.DEFAULT_ENDPOINT,
            version=TestEndpoints.DEFAULT_VERSION,
            type="time_entries",
            arguments="?start_date={start_date}&end_date={end_date}".format(
                start_date=urllib.parse.quote(start_date.isoformat()),
                end_date=urllib.parse.quote(end_date.isoformat())
            )
        )

        if time_entry_url != expected_url:
            self.fail("{} ne {}".format(expected_url, time_entry_url))

    def test_time_entries_current(self):
        time_entry_url = API(version=TestEndpoints.DEFAULT_VERSION).time_entries.current()

        expected_url = TestEndpoints.ENDPOINT_URL_FORMAT.format(
            endpoint=TestEndpoints.DEFAULT_ENDPOINT,
            version=TestEndpoints.DEFAULT_VERSION,
            type="time_entries/current",
            arguments=""
        )

        if time_entry_url != expected_url:
            self.fail("{} ne {}".format(expected_url, time_entry_url))

    def test_projects_base(self):
        projects_url = API(version=TestEndpoints.DEFAULT_VERSION).projects.__repr__()

        expected_url = TestEndpoints.ENDPOINT_URL_FORMAT.format(
            endpoint=TestEndpoints.DEFAULT_ENDPOINT,
            version=TestEndpoints.DEFAULT_VERSION,
            type="projects",
            arguments=""
        )

        if projects_url != expected_url:
            self.fail("{} ne {}".format(expected_url, projects_url))

    def test_projects_details(self):
        project_id = 1

        projects_url = API(version=TestEndpoints.DEFAULT_VERSION).projects.details(identifier=project_id)

        expected_url = TestEndpoints.ENDPOINT_URL_FORMAT.format(
            endpoint=TestEndpoints.DEFAULT_ENDPOINT,
            version=TestEndpoints.DEFAULT_VERSION,
            type="projects",
            arguments="/{}".format(project_id)
        )

        if projects_url != expected_url:
            self.fail("{} ne {}".format(expected_url, projects_url))

    def test_multiple_projects_details(self):
        project_ids = [1, 2, 3, 4]

        projects_url = API(version=TestEndpoints.DEFAULT_VERSION).projects.details(identifiers=project_ids)

        expected_url = TestEndpoints.ENDPOINT_URL_FORMAT.format(
            endpoint=TestEndpoints.DEFAULT_ENDPOINT,
            version=TestEndpoints.DEFAULT_VERSION,
            type="projects",
            arguments="/{}".format(",".join(map(str, project_ids)))
        )

        if projects_url != expected_url:
            self.fail("{} ne {}".format(expected_url, projects_url))

    def test_tags_base(self):
        tags_url = API(version=TestEndpoints.DEFAULT_VERSION).tags.__repr__()

        expected_url = TestEndpoints.ENDPOINT_URL_FORMAT.format(
            endpoint=TestEndpoints.DEFAULT_ENDPOINT,
            version=TestEndpoints.DEFAULT_VERSION,
            type="tags",
            arguments=""
        )

        if tags_url != expected_url:
            self.fail("{} ne {}".format(expected_url, tags_url))

    def test_tags_details(self):
        tag_id = 1

        tags_url = API(version=TestEndpoints.DEFAULT_VERSION).tags.details(tag_id)

        expected_url = TestEndpoints.ENDPOINT_URL_FORMAT.format(
            endpoint=TestEndpoints.DEFAULT_ENDPOINT,
            version=TestEndpoints.DEFAULT_VERSION,
            type="tags",
            arguments="/{}".format(tag_id)
        )

        if tags_url != expected_url:
            self.fail("{} ne {}".format(expected_url, tags_url))

    def test_users_base(self):
        users_url = API(version=TestEndpoints.DEFAULT_VERSION).users.__repr__()

        expected_url = TestEndpoints.ENDPOINT_URL_FORMAT.format(
            endpoint=TestEndpoints.DEFAULT_ENDPOINT,
            version=TestEndpoints.DEFAULT_VERSION,
            type="me",
            arguments=""
        )

        if users_url != expected_url:
            self.fail("{} ne {}".format(expected_url, users_url))

    def test_users_details(self):
        users_url = API(version=TestEndpoints.DEFAULT_VERSION).users.details()

        expected_url = TestEndpoints.ENDPOINT_URL_FORMAT.format(
            endpoint=TestEndpoints.DEFAULT_ENDPOINT,
            version=TestEndpoints.DEFAULT_VERSION,
            type="me",
            arguments=""
        )

        if users_url != expected_url:
            self.fail("{} ne {}".format(expected_url, users_url))

    def test_users_details_with_extra(self):
        users_url = API(version=TestEndpoints.DEFAULT_VERSION).users.details(extra_data=True)

        expected_url = TestEndpoints.ENDPOINT_URL_FORMAT.format(
            endpoint=TestEndpoints.DEFAULT_ENDPOINT,
            version=TestEndpoints.DEFAULT_VERSION,
            type="me",
            arguments="?with_related_data=true"
        )

        if users_url != expected_url:
            self.fail("{} ne {}".format(expected_url, users_url))

    def test_reset_api_token(self):
        users_url = API(version=TestEndpoints.DEFAULT_VERSION).users.reset_api_token()

        expected_url = TestEndpoints.ENDPOINT_URL_FORMAT.format(
            endpoint=TestEndpoints.DEFAULT_ENDPOINT,
            version=TestEndpoints.DEFAULT_VERSION,
            type="reset_token",
            arguments=""
        )

        if users_url != expected_url:
            self.fail("{} ne {}".format(expected_url, users_url))

    def test_workspaces_base(self):
        users_url = API(version=TestEndpoints.DEFAULT_VERSION).workspaces.__repr__()

        expected_url = TestEndpoints.ENDPOINT_URL_FORMAT.format(
            endpoint=TestEndpoints.DEFAULT_ENDPOINT,
            version=TestEndpoints.DEFAULT_VERSION,
            type="workspaces",
            arguments=""
        )

        if users_url != expected_url:
            self.fail("{} ne {}".format(expected_url, users_url))

    def test_workspaces_details(self):
        workspace_id = 1

        users_url = API(version=TestEndpoints.DEFAULT_VERSION).workspaces.details(workspace_id)

        expected_url = TestEndpoints.ENDPOINT_URL_FORMAT.format(
            endpoint=TestEndpoints.DEFAULT_ENDPOINT,
            version=TestEndpoints.DEFAULT_VERSION,
            type="workspaces",
            arguments="/{}".format(workspace_id)
        )

        if users_url != expected_url:
            self.fail("{} ne {}".format(expected_url, users_url))

    def test_workspaces_projects(self):
        workspace_id = 1

        users_url = API(version=TestEndpoints.DEFAULT_VERSION).workspaces.projects(workspace_id)

        expected_url = TestEndpoints.ENDPOINT_URL_FORMAT.format(
            endpoint=TestEndpoints.DEFAULT_ENDPOINT,
            version=TestEndpoints.DEFAULT_VERSION,
            type="workspaces",
            arguments="/{}/projects".format(workspace_id)
        )

        if users_url != expected_url:
            self.fail("{} ne {}".format(expected_url, users_url))

    def test_workspaces_tags(self):
        workspace_id = 1

        users_url = API(version=TestEndpoints.DEFAULT_VERSION).workspaces.tags(workspace_id)

        expected_url = TestEndpoints.ENDPOINT_URL_FORMAT.format(
            endpoint=TestEndpoints.DEFAULT_ENDPOINT,
            version=TestEndpoints.DEFAULT_VERSION,
            type="workspaces",
            arguments="/{}/tags".format(workspace_id)
        )

        if users_url != expected_url:
            self.fail("{} ne {}".format(expected_url, users_url))


if __name__ == '__main__':
    unittest.main()
