import unittest
from datetime import datetime

from toggl.filters import Filters

from toggl.types.project import Project
from toggl.types.workspace import Workspace
from toggl.types.tag import Tag
from toggl.types.time_entry import TimeEntry
from toggl.types.user import User


class TestFilters(unittest.TestCase):
    WORKSPACE_ONE = Workspace(
        name='Test Workspace One',
        identifier=1,
        last_updated=datetime.now())

    WORKSPACE_TWO = Workspace(
        name='Test Workspace Two',
        identifier=2,
        last_updated=datetime.now())

    PROJECT_ONE = Project(
        name='Test Project One',
        color=Project.Color.RED,
        last_updated=datetime.now(),
        created=datetime.now(),
        identifier=1,
        workspace_identifier=1)

    PROJECT_TWO = Project(
        name='Test Project Two',
        color=Project.Color.BLACK,
        last_updated=datetime.now(),
        created=datetime.now(),
        identifier=2,
        workspace_identifier=2)

    TAG_ONE = Tag(
        name='Test Tag One',
        identifier=1,
        workspace_identifier=1)

    TAG_TWO = Tag(
        name='Test Tag Two',
        identifier=2,
        workspace_identifier=1
    )

    TAG_THREE = Tag(
        name='Test Tag Three',
        identifier=3,
        workspace_identifier=1
    )

    TIME_ENTRY_ONE = TimeEntry(
        description='Test Entry One',
        start_time=datetime.now(),
        identifier=1,
        duration=30,
        project_identifier=1,
        workspace_identifier=1,
        stop_time=datetime.now(),
        tags=['Test Tag One', 'Test Tag Two'],
        last_updated=datetime.now()
    )

    TIME_ENTRY_TWO = TimeEntry(
        description='Test Entry Two',
        start_time=datetime.now(),
        identifier=2,
        duration=60,
        project_identifier=1,
        workspace_identifier=1,
        stop_time=datetime.now(),
        tags=['Test Tag Three'],
        last_updated=datetime.now()
    )

    USER = User(
        name='Test User',
        api_token='1234',
        identifier=1,
        last_updated=datetime.now())

    def test_filter_on_workspace_id(self) -> None:
        self.assertEqual([TestFilters.WORKSPACE_ONE],
                         Filters.filter_workspaces_on_id(
                             TestFilters.WORKSPACE_ONE.identifier,
                             [TestFilters.WORKSPACE_ONE, TestFilters.WORKSPACE_TWO]
                         ))

    def test_filter_projects_on_workspace_id(self) -> None:
        self.assertEqual([TestFilters.PROJECT_ONE],
                         Filters.filter_projects_on_workspace_id(
                             TestFilters.WORKSPACE_ONE.identifier,
                             [TestFilters.PROJECT_ONE, TestFilters.PROJECT_TWO]
                         ))

    def test_filter_projects_on_name(self) -> None:
        self.assertEqual([TestFilters.PROJECT_ONE],
                         Filters.filter_projects_on_name(
                             TestFilters.PROJECT_ONE.name,
                             [TestFilters.PROJECT_ONE, TestFilters.PROJECT_TWO]
                         ))

    def test_filter_tags_on_workspace_id(self) -> None:
        self.assertEqual([],
                         Filters.filter_tags_on_workspace_id(
                             TestFilters.WORKSPACE_TWO.identifier,
                             [TestFilters.TAG_ONE, TestFilters.TAG_TWO, TestFilters.TAG_THREE]
                         ))

    def test_filter_tags_on_name(self) -> None:
        self.assertEqual([TestFilters.TAG_TWO],
                         Filters.filter_tags_on_name(
                             TestFilters.TAG_TWO.name,
                             [TestFilters.TAG_ONE, TestFilters.TAG_TWO, TestFilters.TAG_THREE]
                         ))

    def test_filter_tags_on_time_entries(self) -> None:
        self.assertEqual([TestFilters.TAG_ONE, TestFilters.TAG_TWO],
                         Filters.filter_tags_on_time_entries(
                             [TestFilters.TAG_ONE, TestFilters.TAG_TWO],
                             [TestFilters.TIME_ENTRY_ONE, TestFilters.TIME_ENTRY_TWO]
                         ))

    def test_filter_time_entries_on_project_identifier(self) -> None:
        self.assertEqual([TestFilters.TIME_ENTRY_ONE, TestFilters.TIME_ENTRY_TWO],
                         Filters.filter_time_entries_on_project_identifier(
                             TestFilters.PROJECT_ONE.identifier,
                             [TestFilters.TIME_ENTRY_ONE, TestFilters.TIME_ENTRY_TWO]
                         ))

    def test_filter_time_entries_on_tag_name(self) -> None:
        self.assertEqual([TestFilters.TIME_ENTRY_TWO],
                         Filters.filter_time_entries_on_tag_name(
                             TestFilters.TAG_THREE.name,
                             [TestFilters.TIME_ENTRY_ONE, TestFilters.TIME_ENTRY_TWO]
                         ))


if __name__ == '__main__':
    unittest.main()
