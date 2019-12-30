#!/usr/bin/env python

import argparse

import logging
import sys

from tabulate import tabulate

from version import __version__

from toggl.interface import Interface
from arguments import Arguments

from toggl.builders import time_entry_builder
from toggl.builders import tag_builder
from toggl.builders import project_builder

from toggl.downloader import Downloader
from toggl.caching import Caching

if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser(
        prog='python togglcmder',
        description="Control toggl via the REST API. (v{})".format(
            __version__))
    Arguments.insert_main_arguments(argument_parser)

    # adding a nested parser for sub-arguments
    sub_parser = argument_parser.add_subparsers(
        dest='parser_name')
    Arguments.insert_start_timer_arguments(sub_parser)
    Arguments.insert_add_project_arguments(sub_parser)
    Arguments.insert_add_timer_arguments(sub_parser)
    Arguments.insert_add_tag_arguments(sub_parser)

    args = argument_parser.parse_args()
    if len(sys.argv) == 1:
        argument_parser.print_help()
        exit(0)

    logger = logging.getLogger()
    log_file_handle = logging.FileHandler('togglcmder.log')
    log_stream_handle = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s: %(levelname)s: %(module)s: %(lineno)d: %(message)s",
        "%Y-%m-%dT%H:%M:%S")
    log_file_handle.setFormatter(formatter)
    log_stream_handle.setFormatter(formatter)
    logger.addHandler(log_file_handle)
    logger.addHandler(log_stream_handle)

    # formula to convert 0-5 to actual inverted logging levels:
    # User enters 0 -> CRITICAL: 50
    # User enters 1 -> ERROR: 40
    # User enters 2 -> WARN: 30
    # User enters 3 -> INFO: 20
    # User enters 4 -> DEBUG: 10
    logger.setLevel((args.verbosity * -10) + 50)

    token = ""

    if args.token:
        token = args.token
    else:
        try:
            token_file = open('.api_token', 'r')
            token = token_file.read().rstrip()
            token_file.close()
        except FileNotFoundError:
            logger.critical("please create the token file '.api_token'")
            exit(1)

    caching = Caching()
    downloader = Downloader(token)

    user_data = downloader.download_user_data()
    caching.update_user_cache(user_data)

    workspace_data = downloader.download_workspaces()
    caching.update_workspace_cache(workspace_data)

    for workspace in workspace_data:
        tag_data = downloader.download_tags(workspace)
        caching.update_tag_cache(tag_data)

        project_data = downloader.download_projects(workspace)
        caching.update_project_cache(project_data)

    exit(1)

    if args.token_reset:
        token = instance.reset_user_token()
        instance = Interface(api_token=token,
                             logger=logger)

    if token == user_data.api_token and not args.token:
        logger.debug("no token update needed")
    else:
        logger.debug("updating token file")
        file = open('.api_token', 'w')
        file.write(token.replace('"', '').rstrip())
        file.close()

    ## Listing the current running time entry: query API and then update the project/workspace
    ## references. TODO: can be extracted?
    if args.current:
        time_entry = instance.get_current_entry()
        if time_entry is None:
            logger.info("no current time entry")
        else:
            time_entry.project = user_data.get_project_from_id(time_entry.project_id)
            time_entry.workspace = user_data.get_workspace_from_id(time_entry.workspace_id)
            logger.info("\n{}".format(tabulate(
                [time_entry.__str__().split(',')],
                headers=["description", "project", "workspace", "duration", "tags"],
                tablefmt="grid"
            )))

    if args.resume_latest_timer:
        time_entry = user_data.time_entries[-1]
        if time_entry is not None:
            instance.start_time_entry(time_entry)

    if args.stop_timer:
        logger.info("searching for current timer")
        time_entry = instance.get_current_entry()
        if time_entry:
            logger.info("stopping entry: description = '{}'".format(
                time_entry.description
            ))
            instance.stop_time_entry(time_entry)
        else:
            logging.info("no running entry")

    if args.parser_name == 'start-timer':
        try:
            time_entry = user_data.find_time_entry(
                args.description,
                args.workspace,
                args.project)
            logger.warning('time entry already exists')
            instance.start_time_entry(time_entry)
        except ValueError:
            if args.workspace:
                workspace = user_data.find_workspace(args.workspace)
            else:
                workspace = None
            if args.project:
                project = user_data.find_user_project(args.project)
            else:
                project = None
            if args.tags:
                tags = args.tags.split(',')
            else:
                tags = None
            time_entry = time_entry_builder.TimeEntryBuilder.from_now(
                workspace, project, args.description, tags)
            instance.start_time_entry(time_entry)

    elif args.parser_name == 'add-tag':
        try:
            user_data.find_tag(
                args.name,
                args.workspace)
        except ValueError:
            workspace = user_data.find_workspace(args.workspace)
            tag = tag_builder.TagBuilder.from_name_and_workspace(
                args.name,
                workspace)
            instance.create_tag(tag)

    elif args.parser_name == 'add-project':
        try:
            user_data.find_project(
                args.name,
                args.workspace)
        except ValueError:
            workspace = user_data.find_workspace(args.workspace)
            project = project_builder.ProjectBuilder.from_name_and_workspace(
                args.name, workspace)
            instance.create_project(project)

    ## The following code covers listing items.
    ## TODO: can be extracted?
    if args.list_workspaces:
        workspaces = instance.download_workspaces()
        if workspaces:
            logger.info("\n{}".format(tabulate(
                [s.__str__().split(',') for s in workspaces],
                headers=["name"],
                tablefmt="grid"
            )))
        else:
            logger.info("no workspaces found")

    if args.list_projects:
        # projects = instance.download_projects(user_data.get_workspace_from_id())
        if user_data.projects:
            logger.info("\n{}".format(tabulate(
                [s.__str__().split(',') for s in user_data.projects],
                headers=["name","workspace"],
                tablefmt="grid"
            )))
        else:
            logger.info("no projects found")

    if args.list_tags:
        if user_data.tags:
            logger.info("\n{}".format(tabulate(
                [s.__str__().split(',') for s in user_data.tags],
                headers=["name", "workspace"],
                tablefmt="grid"
            )))
        else:
            logger.info("no tags found")

    if args.list_time_entries:
        if user_data.time_entries:
            logger.info("\n{}".format(tabulate(
                [s.__str__().split(',') for s in user_data.time_entries],
                headers=["description", "project", "workspace", "duration", "tags"],
                tablefmt="grid"
            )))
        else:
            logger.info("no time entries found")