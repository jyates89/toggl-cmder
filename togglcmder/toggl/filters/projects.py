from typing import List
import re as regex
import logging

from togglcmder.toggl.types.project import Project
from togglcmder.toggl.types.workspace import Workspace


class Projects(object):

    @staticmethod
    def filter_single(
            projects: List[Project],
    ) -> Project:
        if not projects:
            raise RuntimeError('no projects passed in when single project expected')
        elif len(projects) > 1:
            raise RuntimeError('multiple projects passed in when single project expected')

        return projects[0]

    @staticmethod
    def filter_on_name(
            projects: List[Project],
            name: str
    ) -> List[Project]:
        logger = logging.getLogger(__name__)
        if not name:
            logger.debug('no name provided for filter_on_name(projects) with input = {}'.format(
                    [project.name for project in projects]
                ))
            return projects

        result = list(filter(
            lambda project:
                regex.match("^{}$".format(name),
                            project.name,
                            regex.IGNORECASE),
            projects
        ))

        if not result:
            logger.warning('no projects found with name = {} and with input = {}'.format(
                name, [project.name for project in projects]
            ))
        return result

    @staticmethod
    def filter_on_workspace(
            projects: List[Project],
            workspace: Workspace
    ) -> List[Project]:
        logger = logging.getLogger(__name__)
        if not workspace:
            logger.debug('no workspace provided for filter_on_workspace(projects) with input = {}'.format(
                [(project.name, project.workspace_identifier) for project in projects]
            ))
            return projects

        result = list(filter(
            lambda project: workspace.identifier == project.workspace_identifier,
            projects
        ))

        if not result:
            logger.warning('no projects found with workspace = {} and with input = {}'.format(
                (workspace.name, workspace.identifier),
                [(project.name, project.workspace_identifier) for project in projects]
            ))
        return result

    @staticmethod
    def filter_on_color(
            projects: List[Project],
            color: Project.Color
    ) -> List[Project]:
        logger = logging.getLogger(__name__)
        if not color:
            logger.debug('no color provided for filter_on_color(projects) with input = {}'.format(
                [(project.name, project.color.name) for project in projects]
            ))
            return projects

        result = list(filter(
            lambda project: color == project.color,
            projects
        ))

        if not result:
            logger.warning('no projects found with color = {} and with input = {}'.format(
                color.name, [(project.name, project.color.name) for project in projects]
            ))
        return result

    @staticmethod
    def filter_on_identifier(
            projects: List[Project],
            identifier: int
    ) -> List[Project]:
        logger = logging.getLogger(__name__)
        if not identifier:
            logger.debug('no identifier provided for filter_on_identifier(projects) with input = {}'.format(
                [(project.name, project.identifier) for project in projects]
            ))
            return projects

        result = list(filter(
            lambda project: identifier == project.identifier,
            projects
        ))

        if not result:
            logger.warning('no projects found with identifier = {} and with input = {}'.format(
                identifier, [(project.name, project.identifier) for project in projects]
            ))
        return result
