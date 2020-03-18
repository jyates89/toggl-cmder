from typing import List
import re as regex
import logging

from togglcmder.toggl.types.workspace import Workspace


class Workspaces(object):

    @staticmethod
    def filter_single(
            workspaces: List[Workspace],
    ) -> Workspace:
        if not workspaces:
            raise RuntimeError('no workspaces passed in when single workspace expected')
        elif len(workspaces) > 1:
            raise RuntimeError('multiple workspaces passed in when single workspace expected')

        return workspaces[0]

    @staticmethod
    def filter_on_name(
            workspaces: List[Workspace],
            name: str
    ) -> List[Workspace]:
        logger = logging.getLogger(__name__)
        if not name:
            logger.debug('no name provided for filter_on_name(workspaces) with input = {}'.format(
                [workspace.name for workspace in workspaces]
            ))
            return workspaces

        result = list(filter(
            lambda workspace:
                regex.match("^{}$".format(name),
                            workspace.name,
                            regex.IGNORECASE),
            workspaces
        ))

        if not result:
            logger.warning('no workspaces found with name = {} and with input = {}'.format(
                name, [workspace.name for workspace in workspaces]
            ))
        return result

    @staticmethod
    def filter_on_identifier(
            workspaces: List[Workspace],
            identifier: int
    ) -> List[Workspace]:
        logger = logging.getLogger(__name__)
        if not identifier:
            logger.debug('no identifier provided for filter_on_identifier(workspaces) with input = {}'.format(
                [workspace.name for workspace in workspaces]
            ))
            return workspaces

        result = list(filter(
            lambda workspace: identifier == workspace.identifier,
            workspaces
        ))

        if not result:
            logger.warning('no workspaces found with identifier = {} and with input = {}'.format(
                identifier, [workspace.name for workspace in workspaces]
            ))
        return result
