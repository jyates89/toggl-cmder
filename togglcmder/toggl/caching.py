import sqlite3
from sqlite3 import IntegrityError

from typing import List
from datetime import datetime

from toggl.types.workspace import Workspace
from toggl.types.time_entry import TimeEntry
from toggl.types.user import User
from toggl.types.tag import Tag
from toggl.types.project import Project


class Caching(object):
    WORKSPACE_TABLE = '''
    CREATE TABLE IF NOT EXISTS workspaces (
        name TEXT NOT NULL,
        identifier INTEGER PRIMARY KEY,
        last_updated TIMESTAMP NOT NULL
    )
    '''

    PROJECT_TABLE = '''
    CREATE TABLE IF NOT EXISTS projects (
        name TEXT NOT NULL,
        color INTEGER,
        last_updated TIMESTAMP NOT NULL,
        created TIMESTAMP NOT NULL,
        identifier INTEGER PRIMARY KEY,
        workspace_identifier INTEGER NOT NULL,
        FOREIGN KEY (workspace_identifier) REFERENCES workspaces (identifier)
    )
    '''

    TAG_TABLE = '''
    CREATE TABLE IF NOT EXISTS tags (
        name TEXT,
        identifier INTEGER PRIMARY KEY,
        workspace_identifier INTEGER,
        FOREIGN KEY (workspace_identifier) REFERENCES workspaces (identifier)
    )
    '''

    TIME_ENTRY_TABLE = '''
    CREATE TABLE IF NOT EXISTS time_entries (
        description TEXT,
        start_time TIMESTAMP NOT NULL,
        stop_time TIMESTAMP,
        duration INTEGER,
        identifier INTEGER PRIMARY KEY,
        project_identifier INTEGER,
        workspace_identifier INTEGER NOT NULL,
        last_updated TIMESTAMP,
        FOREIGN KEY (project_identifier) REFERENCES projects (identifier),
        FOREIGN KEY (workspace_identifier) REFERENCES workspaces (identifier)
    )
    '''

    TIME_ENTRY_TAG_JUNCTION_TABLE = '''
    CREATE TABLE IF NOT EXISTS time_entry_tags (
        tag_identifier INTEGER NOT NULL,
        time_entry_identifier INTEGER NOT NULL,
        FOREIGN KEY (tag_identifier) REFERENCES tags (identifier),
        FOREIGN KEY (time_entry_identifier) REFERENCES time_entries (identifier)
    )
    '''

    USER_TABLE = '''
    CREATE TABLE IF NOT EXISTS users (
        name TEXT,
        api_token TEXT,
        identifier INTEGER PRIMARY KEY,
        last_updated TIMESTAMP NOT NULL
    )
    '''

    def __init__(self, *, cache_name: str = "cache.db"):
        self.__connection = sqlite3.connect(cache_name)
        self.__cursor = self.__connection.cursor()

        self.__cursor.execute("PRAGMA foreign_keys = 1")
        self.__connection.commit()

        self.__cursor.execute(Caching.WORKSPACE_TABLE)
        self.__cursor.execute(Caching.PROJECT_TABLE)
        self.__cursor.execute(Caching.TAG_TABLE)
        self.__cursor.execute(Caching.TIME_ENTRY_TABLE)
        self.__cursor.execute(Caching.TIME_ENTRY_TAG_JUNCTION_TABLE)
        self.__cursor.execute(Caching.USER_TABLE)

        self.__connection.commit()

    def __del__(self):
        self.__connection.close()

    def update_workspace_cache(self, workspaces: List[Workspace]) -> int:
        insert_sql = '''
            INSERT INTO workspaces
            (name, identifier, last_updated) VALUES 
            (?, ?, ?)
        '''

        update_sql = '''
            UPDATE workspaces SET name=?, last_updated=?
            WHERE identifier=?
        '''

        for workspace in workspaces:
            try:
                self.__cursor.execute(
                    insert_sql, (workspace.name,
                                 workspace.identifier,
                                 workspace.last_updated.timestamp()))
            except IntegrityError:
                self.__cursor.execute(
                    update_sql, (workspace.name,
                                 workspace.last_updated.timestamp(),
                                 workspace.identifier))

        self.__connection.commit()
        return self.__cursor.rowcount

    def retrieve_workspace_cache(self) -> List[Workspace]:
        sql = '''
            SELECT name, identifier, last_updated FROM workspaces
        '''

        self.__cursor.execute(sql)
        results = self.__cursor.fetchall()
        if results:
            return [
                Workspace(
                    name=result[0],
                    identifier=result[1],
                    last_updated=datetime.fromtimestamp(result[2])
                ) for result in results
            ]

    def update_user_cache(self, user: User) -> int:
        insert_sql = '''
            INSERT INTO users
            (name, api_token, identifier, last_updated) VALUES 
            (?, ?, ?, ?)
        '''

        update_sql = '''
            UPDATE users SET name=?, api_token=?, last_updated=?
            WHERE identifier=?
        '''

        try:
            self.__cursor.execute(
                insert_sql, (user.name,
                             user.api_token,
                             user.identifier,
                             user.last_updated.timestamp()))
        except IntegrityError:
            self.__cursor.execute(
                update_sql, (user.name,
                             user.api_token,
                             user.last_updated.timestamp(),
                             user.identifier))

        self.__connection.commit()
        return self.__cursor.rowcount

    def retrieve_user_cache(self) -> User:
        sql = '''
            SELECT name, api_token, identifier, last_updated FROM users
        '''

        self.__cursor.execute(sql)
        results = self.__cursor.fetchone()
        if results:
            return User(
                name=results[0],
                api_token=results[1],
                identifier=results[2],
                last_updated=datetime.fromtimestamp(results[3])
            )

    def update_project_cache(self, projects: List[Project]) -> int:
        insert_sql = '''
            INSERT INTO projects
            (name, color, last_updated, created, identifier, workspace_identifier) VALUES 
            (?, ?, ?, ?, ?, ?) 
        '''

        update_sql = '''
            UPDATE projects
            SET name=?, color=?, last_updated=?, workspace_identifier=?
            WHERE identifier=?
        '''

        for project in projects:
            try:
                self.__cursor.execute(
                    insert_sql, (project.name,
                                 project.color.value,
                                 project.last_updated.timestamp(),
                                 project.created.timestamp(),
                                 project.identifier,
                                 project.workspace_identifier))
            except IntegrityError:
                self.__cursor.execute(
                    update_sql, (project.name,
                                 project.color.value,
                                 project.last_updated.timestamp(),
                                 project.workspace_identifier,
                                 project.identifier))

        self.__connection.commit()
        return self.__cursor.rowcount

    def retrieve_project_cache(self) -> List[Project]:
        sql = '''
            SELECT name, color, last_updated, created, identifier, workspace_identifier FROM projects
        '''

        self.__cursor.execute(sql)
        results = self.__cursor.fetchall()
        if results:
            return [
                Project(
                    name=result[0],
                    color=Project.Color(result[1]),
                    last_updated=datetime.fromtimestamp(result[2]),
                    created=datetime.fromtimestamp(result[3]),
                    identifier=result[4],
                    workspace_identifier=result[5]
                ) for result in results
            ]

    def update_tag_cache(self, tags: List[Tag]) -> int:
        insert_sql = '''
            INSERT INTO tags
            (name, identifier, workspace_identifier) VALUES
            (?, ?, ?)
        '''

        update_sql = '''
            UPDATE tags
            SET name=?, workspace_identifier=?
            WHERE identifier=?
        '''

        rows_affected=0
        for tag in tags:
            try:
                self.__cursor.execute(
                    insert_sql, (tag.name,
                                 tag.identifier,
                                 tag.workspace_identifier))
            except IntegrityError:
                self.__cursor.execute(
                    update_sql, (tag.name,
                                 tag.workspace_identifier,
                                 tag.identifier))
            rows_affected += self.__cursor.rowcount

        self.__connection.commit()
        return rows_affected

    def retrieve_tag_cache(self) -> List[Tag]:
        sql = """
            SELECT name, identifier, workspace_identifier FROM tags
        """

        self.__cursor.execute(sql)
        results = self.__cursor.fetchall()
        if results:
            return [
                Tag(
                    name=result[0],
                    identifier=result[1],
                    workspace_identifier=result[2]
                ) for result in results
            ]

    def __retrieve_time_entry_tags_join(self, time_entry_identifier: int) -> List[tuple]:
        sql = '''
            SELECT name, tag_identifier, time_entry_identifier
            FROM time_entry_tags
            INNER JOIN tags ON time_entry_tags.tag_identifier = tags.identifier
            WHERE time_entry_identifier=?
        '''
        self.__cursor.execute(sql, (time_entry_identifier,))
        return self.__cursor.fetchall()

    def __retrieve_time_entry_tags(self, time_entry_identifier: int) -> List[tuple]:
        sql = '''
            SELECT tag_identifier, time_entry_identifier
            FROM time_entry_tags
            WHERE time_entry_identifier=?
        '''
        self.__cursor.execute(sql, (time_entry_identifier,))
        return self.__cursor.fetchall()

    def __check_existing(self, tags: List[int], time_entry_identifier: int) -> List[int]:
        # returns a tuple of (tag_id, time_entry_id)
        existing_time_entry_tags = self.__retrieve_time_entry_tags(time_entry_identifier)
        if len(tags) == 0 or len(existing_time_entry_tags) == 0:
            return tags
        return list(
            # 2. map each tuple to be just the tag identifier, so given x,
            #    return the tag_id
            map(lambda x: x[0],
                # 1. filter so we only get tags tuples that aren't in the existing list
                #     of tags (checked based on x[0], which is the tag identifier)
                filter(lambda x: x[0] not in tags, existing_time_entry_tags)))

    def update_time_entry_cache(self, time_entries: List[TimeEntry]) -> int:
        insert_sql = '''
            INSERT INTO time_entries
            (description, start_time, stop_time, duration, identifier,
             project_identifier, workspace_identifier, last_updated) VALUES 
            (?, ?, ?, ?, ?, ?, ?, ?)
        '''

        update_sql = '''
            UPDATE time_entries
            SET description=?, 
                start_time=?, 
                stop_time=?, 
                duration=?, 
                project_identifier=?, 
                workspace_identifier=?, 
                last_updated=?
            WHERE identifier=?
        '''

        insert_time_entry_tag_sql = '''
            INSERT INTO time_entry_tags
            (tag_identifier, time_entry_identifier)
            VALUES (?, ?)
        '''
        tag_rows = self.retrieve_tag_cache()
        rows_affected = 0


        for time_entry in time_entries:
            try:
                self.__cursor.execute(
                    insert_sql, (time_entry.description,
                                 time_entry.start_time.timestamp(),
                                 time_entry.stop_time.timestamp(),
                                 time_entry.duration,
                                 time_entry.identifier,
                                 time_entry.project_identifier,
                                 time_entry.workspace_identifier,
                                 time_entry.last_updated.timestamp()))
            except IntegrityError:
                self.__cursor.execute(
                    update_sql, (time_entry.description,
                                 time_entry.start_time.timestamp(),
                                 time_entry.stop_time.timestamp(),
                                 time_entry.duration,
                                 time_entry.project_identifier,
                                 time_entry.workspace_identifier,
                                 time_entry.last_updated.timestamp(),
                                 time_entry.identifier))
            rows_affected += self.__cursor.rowcount

            tag_ids = []
            for tag in time_entry.tags:
                for tag_row in tag_rows:
                    if tag == tag_row.name:
                        tag_ids.append(tag_row.identifier)
                        break
            for tag_id in self.__check_existing(tag_ids, time_entry.identifier):
                self.__cursor.execute(
                    insert_time_entry_tag_sql,
                    (tag_id,
                     time_entry.identifier))

        self.__connection.commit()

        return rows_affected

    def retrieve_time_entry_cache(self) -> List[TimeEntry]:
        time_entry_sql = """
            SELECT  description, 
                    start_time, 
                    stop_time, 
                    duration, 
                    identifier, 
                    project_identifier, 
                    workspace_identifier, 
                    last_updated
            FROM time_entries
        """

        time_entries = []

        self.__cursor.execute(time_entry_sql)
        results = self.__cursor.fetchall()
        for result in results:
            tag_results = self.__retrieve_time_entry_tags_join(result[4])
            time_entries.append(TimeEntry(
                description=result[0],
                start_time=datetime.fromtimestamp(result[1]),
                stop_time=datetime.fromtimestamp(result[2]),
                duration=result[3],
                identifier=result[4],
                project_identifier=result[5],
                workspace_identifier=result[6],
                last_updated=datetime.fromtimestamp(result[7]),
                tags=[tag_result[0] for tag_result in tag_results]
            ))

        return time_entries
