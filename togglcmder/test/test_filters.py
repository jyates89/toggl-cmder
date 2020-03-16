import unittest
from datetime import datetime

from togglcmder.toggl.filters.time_entries import TimeEntries
from togglcmder.toggl.filters.tags import Tags
from togglcmder.toggl.filters.workspaces import Workspaces
from togglcmder.toggl.filters.projects import Projects

from togglcmder.toggl.types.project import Project
from togglcmder.toggl.types.workspace import Workspace
from togglcmder.toggl.types.tag import Tag
from togglcmder.toggl.types.time_entry import TimeEntry
from togglcmder.toggl.types.user import User


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
                         Workspaces.filter_on_identifier(
                             [TestFilters.WORKSPACE_ONE, TestFilters.WORKSPACE_TWO],
                             TestFilters.WORKSPACE_ONE.identifier
                         ))

    def test_filter_projects_on_workspace(self) -> None:
        self.assertEqual([TestFilters.PROJECT_ONE],
                         Projects.filter_on_workspace(
                             [TestFilters.PROJECT_ONE, TestFilters.PROJECT_TWO],
                             TestFilters.WORKSPACE_ONE
                         ))

    def test_filter_projects_on_name(self) -> None:
        self.assertEqual([TestFilters.PROJECT_ONE],
                         Projects.filter_on_name(
                             [TestFilters.PROJECT_ONE, TestFilters.PROJECT_TWO],
                             TestFilters.PROJECT_ONE.name
                         ))

    def test_filter_tags_on_workspace(self) -> None:
        self.assertEqual([],
                         Tags.filter_on_workspace(
                             [TestFilters.TAG_ONE, TestFilters.TAG_TWO, TestFilters.TAG_THREE],
                             TestFilters.WORKSPACE_TWO
                         ))

    def test_filter_tags_on_name(self) -> None:
        self.assertEqual([TestFilters.TAG_TWO],
                         Tags.filter_on_name(
                             [TestFilters.TAG_ONE, TestFilters.TAG_TWO, TestFilters.TAG_THREE],
                             TestFilters.TAG_TWO.name
                         ))

    def test_filter_time_entries_on_project(self) -> None:
        self.assertEqual([TestFilters.TIME_ENTRY_ONE, TestFilters.TIME_ENTRY_TWO],
                         TimeEntries.filter_on_project(
                             [TestFilters.TIME_ENTRY_ONE, TestFilters.TIME_ENTRY_TWO],
                             TestFilters.PROJECT_ONE
                         ))

    def test_filter_time_entries_on_tag_name(self) -> None:
        self.assertEqual([TestFilters.TIME_ENTRY_TWO],
                         TimeEntries.filter_on_any_tags(
                             [TestFilters.TIME_ENTRY_ONE, TestFilters.TIME_ENTRY_TWO],
                             [TestFilters.TAG_THREE]
                         ))


if __name__ == '__main__':
    unittest.main()
