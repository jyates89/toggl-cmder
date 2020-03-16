from typing import List
import re as regex
import logging

from togglcmder.toggl.types.workspace import Workspace
from togglcmder.toggl.types.tag import Tag


class Tags(object):

    @staticmethod
    def filter_single(
            tags: List[Tag],
    ) -> Tag:
        if not tags:
            raise RuntimeError('no tags passed in when single tag expected')
        elif len(tags) > 1:
            raise RuntimeError('multiple tags passed in when single tag expected')

        return tags[0]

    @staticmethod
    def filter_on_name(
            tags: List[Tag],
            name: str
    ) -> List[Tag]:
        logger = logging.getLogger(__name__)
        if not name:
            logger.debug('no name provided for filter_on_name(tags) with input = {}'.format(
                [tag.name for tag in tags]
            ))
            return tags

        result = list(filter(
            lambda tag:
                regex.match("^{}$".format(name),
                            tag.name,
                            regex.IGNORECASE),
            tags
        ))

        if not result:
            logger.warning('no tags found with name = {} and with input = {}'.format(
                name, [tag.name for tag in tags]
            ))
        return result

    @staticmethod
    def filter_on_names(
            tags: List[Tag],
            names: List[str]
    ) -> List[Tag]:
        logger = logging.getLogger(__name__)
        if not names:
            logger.debug('no names provided for filter_on_names(tags) with input = {}'.format(
                [tag.name for tag in tags]
            ))
            return tags

        result = list(filter(
            lambda tag: tag.name in names,
            tags
        ))

        if not result:
            logger.warning('no tags found with names = {} and with input = {}'.format(
                names, [tag.name for tag in tags]
            ))
        return result

    @staticmethod
    def filter_on_workspace(
            tags: List[Tag],
            workspace: Workspace
    ) -> List[Tag]:
        logger = logging.getLogger(__name__)
        if not workspace:
            logger.debug('no workspace provided for filter_on_workspace(tags) with input = {}'.format(
                [(tag.name, tag.workspace_identifier) for tag in tags]
            ))
            return tags

        result = list(filter(
            lambda tag: workspace.identifier == tag.workspace_identifier,
            tags
        ))

        if not result:
            logger.warning('no tags found with workspace = {} and with input = {}'.format(
                (workspace.name, workspace.identifier), [(tag.name, tag.workspace_identifier) for tag in tags]
            ))
        return result

    @staticmethod
    def filter_on_identifier(
            tags: List[Tag],
            identifier: int
    ) -> List[Tag]:
        logger = logging.getLogger(__name__)
        if not identifier:
            logger.debug('no identifier provided for filter_on_identifier(tags) with input = {}'.format(
                [(tag.name, tag.identifier) for tag in tags]
            ))
            return tags

        result = list(filter(
            lambda tag: identifier == tag.identifier,
            tags
        ))

        if not result:
            logger.warning('no tags found with identifier = {} and with input = {}'.format(
                identifier, [(tag.name, tag.identifier) for tag in tags]
            ))
        return result
