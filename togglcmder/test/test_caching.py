import unittest
from datetime import datetime

from toggl.caching import Caching
from toggl.types.workspace import Workspace
from toggl.types.project import Project
from toggl.types.tag import Tag
from toggl.types.user import User
from toggl.types.time_entry import TimeEntry


class TestCaching(unittest.TestCase):
    WORKSPACE = Workspace(
        name='Test Workspace',
        identifier=1,
        last_updated=datetime.now())

    PROJECT = Project(
        name='Test Project',
        color=Project.Color.RED,
        last_updated=datetime.now(),
        created=datetime.now(),
        identifier=1,
        workspace_identifier=1)

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

    def setUp(self) -> None:
        self.__connection = Caching(cache_name=':memory:')

    def tearDown(self) -> None:
        del self.__connection

    def test_workspace_caching(self):
        self.assertEqual(1, self.__connection.update_workspace_cache([TestCaching.WORKSPACE]))
        self.assertEqual([TestCaching.WORKSPACE], self.__connection.retrieve_workspace_cache())

    def test_project_caching(self):
        self.assertEqual(1, self.__connection.update_workspace_cache([TestCaching.WORKSPACE]))
        self.assertEqual(1, self.__connection.update_project_cache([TestCaching.PROJECT]))
        self.assertEqual([TestCaching.PROJECT], self.__connection.retrieve_project_cache())

    def test_tag_caching(self):
        self.assertEqual(1, self.__connection.update_workspace_cache([TestCaching.WORKSPACE]))
        self.assertEqual(3, self.__connection.update_tag_cache([TestCaching.TAG_ONE,
                                                             TestCaching.TAG_TWO,
                                                             TestCaching.TAG_THREE]))
        self.assertEqual([TestCaching.TAG_ONE,
                          TestCaching.TAG_TWO,
                          TestCaching.TAG_THREE], self.__connection.retrieve_tag_cache())

    def test_time_entry_caching(self):
        self.assertEqual(1, self.__connection.update_workspace_cache([TestCaching.WORKSPACE]))
        self.assertEqual(1, self.__connection.update_project_cache([TestCaching.PROJECT]))
        self.assertEqual(3, self.__connection.update_tag_cache(
            [TestCaching.TAG_ONE, TestCaching.TAG_TWO, TestCaching.TAG_THREE]))
        self.assertEqual(2, self.__connection.update_time_entry_cache(
            [TestCaching.TIME_ENTRY_ONE, TestCaching.TIME_ENTRY_TWO]))
        self.assertEqual([TestCaching.TIME_ENTRY_ONE, TestCaching.TIME_ENTRY_TWO],
                         self.__connection.retrieve_time_entry_cache())

    def test_user_caching(self):
        self.assertEqual(1, self.__connection.update_workspace_cache([TestCaching.WORKSPACE]))
        self.assertEqual(1, self.__connection.update_user_cache(TestCaching.USER))
        self.assertEqual(TestCaching.USER, self.__connection.retrieve_user_cache())


if __name__ == '__main__':
    unittest.main()
