from datetime import datetime
import re as regex
from typing import List
import logging

from togglcmder.toggl.types.workspace import Workspace
from togglcmder.toggl.types.project import Project
from togglcmder.toggl.types.tag import Tag
from togglcmder.toggl.types.time_entry import TimeEntry


class TimeEntries(object):

    @staticmethod
    def filter_single(
            time_entries: List[TimeEntry],
    ) -> TimeEntry:
        if not time_entries:
            raise RuntimeError('no time entries passed in when single time entry expected')
        elif len(time_entries) > 1:
            raise RuntimeError('multiple time entries passed in when single time entry expected')

        return time_entries[0]

    @staticmethod
    def filter_on_description(
            time_entries: List[TimeEntry],
            description: str
    ) -> List[TimeEntry]:
        logger = logging.getLogger(__name__)
        if not description:
            logger.debug('no description provided for filter_on_description(time_entries) with input = {}'.format(
                [entry.description for entry in time_entries]
            ))
            return time_entries

        result = list(filter(
            lambda time_entry:
                regex.match("^{}$".format(description),
                            time_entry.description if time_entry.description else "",
                            regex.IGNORECASE),
            time_entries
        ))

        if not result:
            logger.warning('no time entries found with description = {} and with input = {}'.format(
                description, [entry.description for entry in time_entries]
            ))
        return result

    @staticmethod
    def filter_on_workspace(
            time_entries: List[TimeEntry],
            workspace: Workspace
    ) -> List[TimeEntry]:
        logger = logging.getLogger(__name__)
        if not workspace:
            logger.debug('no workspace provided for filter_on_workspace(time_entries) with input = {}'.format(
                [(entry.description, entry.workspace_identifier) for entry in time_entries]
            ))
            return time_entries

        result = list(filter(
            lambda time_entry: workspace.identifier == time_entry.workspace_identifier,
            time_entries
        ))

        if not result:
            logger.warning('no time entries found with workspace = {} and with input = {}'.format(
                (workspace.name, workspace.identifier),
                [(entry.description, entry.workspace_identifier) for entry in time_entries]
            ))
        return result

    @staticmethod
    def filter_on_project(
            time_entries: List[TimeEntry],
            project: Project
    ) -> List[TimeEntry]:
        logger = logging.getLogger(__name__)
        if not project:
            logger.debug('no project provided for filter_on_project(time_entries) with input = {}'.format(
                [(entry.description, entry.project_identifier) for entry in time_entries]
            ))
            return time_entries

        result = list(filter(
            lambda time_entry: project.identifier == time_entry.project_identifier,
            time_entries
        ))

        if not result:
            logger.warning('no time entries found with project = {} and with input = {}'.format(
                (project.name, project.identifier),
                [(entry.description, entry.project_identifier) for entry in time_entries]
            ))
        return result

    @staticmethod
    def filter_on_all_tags(
            time_entries: List[TimeEntry],
            tags: List[Tag]
    ) -> List[TimeEntry]:
        logger = logging.getLogger(__name__)
        if not tags:
            logger.debug('no tags provided for filter_on_all_tags(time_entries) with input = {}'.format(
                [entry.tags for entry in time_entries]
            ))
            return time_entries

        result = list(filter(
            lambda time_entry: set(
                [tag.name for tag in tags]
            ).issubset(time_entry.tags),
            time_entries
        ))

        if not result:
            logger.warning('no time entries found with tags = {} and with input = {}'.format(
                [tag.name for tag in tags], [entry.tags for entry in time_entries]
            ))
        return result

    @staticmethod
    def filter_on_any_tags(
            time_entries: List[TimeEntry],
            tags: List[Tag]
    ) -> List[TimeEntry]:
        logger = logging.getLogger(__name__)
        if not tags:
            logger.debug('no tags provided for filter_on_any_tags(time_entries) with input = {}'.format(
                [entry.tags for entry in time_entries]
            ))
            return time_entries

        result = list(filter(
            lambda time_entry:
                not set([tag.name for tag in tags]).isdisjoint(time_entry.tags),
            time_entries
        ))

        if not result:
            logger.warning('no time entries found with tags = {} and with input = {}'.format(
                [tag.name for tag in tags], [entry.tags for entry in time_entries]
            ))
        return result

    @staticmethod
    def filter_on_date_range(
            time_entries: List[TimeEntry],
            start: datetime,
            end: datetime
    ) -> List[TimeEntry]:
        logger = logging.getLogger(__name__)
        if not start and not end:
            logger.debug('neither start nor end provided for filter_on_date_range(time_entries) with input = {}'.format(
                [(entry.start_time.isoformat(), entry.stop_time.isoformat()) for entry in time_entries]
            ))
            return time_entries

        result = None
        if start and end:
            result = list(filter(
                lambda time_entry: start < time_entry.start_time < end,
                time_entries
            ))
            if not result:
                logger.warning('no time entries found for start = {} and end = {} and with input = {}'.format(
                    start.isoformat(), end.isoformat(),
                    [entry.start_time.isoformat() for entry in time_entries]
                ))

        elif start:
            result = list(filter(
                lambda time_entry: start < time_entry.start_time,
                time_entries
            ))
            if not result:
                logger.warning('no time entries found with start = {} and with input = {}'.format(
                    start.isoformat(), [entry.start_time.isoformat() for entry in time_entries]
                ))

        elif end:
            result = list(filter(
                lambda time_entry: time_entry.start_time < end,
                time_entries
            ))
            if not result:
                logger.warning('no time entries found with end = {} and with input = {}'.format(
                    end.isoformat(), [entry.stop_time.isoformat() for entry in time_entries]
                ))

        return result
