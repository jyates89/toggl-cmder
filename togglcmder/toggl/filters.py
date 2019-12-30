from typing import List
import re

from toggl.types.workspace import Workspace
from toggl.types.project import Project
from toggl.types.tag import Tag
from toggl.types.time_entry import TimeEntry


class Filters(object):
    """

    """
    @staticmethod
    def filter_workspaces_on_id(workspace_id: int, workspaces: List[Workspace]) -> List[Workspace]:
        return list(filter(
            lambda workspace: workspace_id == workspace.identifier, workspaces
        ))

    @staticmethod
    def filter_projects_on_workspace_id(workspace_id: int, projects: List[Project]) -> List[Project]:
        return list(filter(
            lambda project: workspace_id == project.workspace_identifier, projects
        ))

    @staticmethod
    def filter_projects_on_name(project_name: str, projects: List[Project]) -> List[Project]:
        return list(filter(
            lambda project: re.search("^{}$".format(project_name), project.name, re.IGNORECASE),
            projects
        ))

    # filter on workspace
    @staticmethod
    def filter_tags_on_workspace_id(workspace_id: int, tags: List[Tag]) -> List[Tag]:
        return list(filter(
            lambda tag: workspace_id == tag.workspace_identifier,
            tags))

    # filter on tag name
    @staticmethod
    def filter_tags_on_name(tag_name: str, tags: List[Tag]) -> List[Tag]:
        return list(filter(
            lambda tag: re.search(tag_name, tag.name, re.IGNORECASE),
            tags))

    # filter tag on time entries
    @staticmethod
    def filter_tags_on_time_entries(tags: List[Tag], time_entries: List[TimeEntry]) -> List[Tag]:
        return list(filter(
            lambda tag: len(Filters.filter_time_entries_on_tag_name(tag.name, time_entries)) != 0,
            tags))

    # filter time entries on project name
    @staticmethod
    def filter_time_entries_on_project_identifier(project_identifier: int, time_entries: List[TimeEntry]) -> List[TimeEntry]:
        return list(filter(
            lambda time_entry: time_entry.project_identifier == project_identifier,
            time_entries))

    # filter time entries on tag
    @staticmethod
    def filter_time_entries_on_tag_name(tag_name: str, time_entries: List[TimeEntry]) -> List[TimeEntry]:
        return list(filter(
            lambda time_entry: tag_name in time_entry.tags,
            time_entries))
