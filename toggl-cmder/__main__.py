import argparse

import logging
import sys

from tabulate import tabulate

from version import __version__

from toggl.interface import Interface
from toggl.arguments import Arguments

from toggl.builders import time_entry_builder
from toggl.builders import tag_builder
from toggl.builders import project_builder

if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser(
        prog='python toggl-cmder',
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
    log_file_handle = logging.FileHandler('toggl-cmder.log')
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

    instance = Interface(api_token=token,
                         logger=logger)
    if not instance.test_connection():
        raise RuntimeError("authentication failure")

    user_data = instance.download_user_data()

    if args.token_reset:
        token = instance.reset_user_token()
        instance = Interface(api_token=token,
                             logger=logger)

    if token == user_data.api_token and not args.token:
        logger.info("no token update needed")
    else:
        logger.info("updating token file")
        file = open('.api_token', 'w')
        file.write(token.replace('"', '').rstrip())
        file.close()

    if args.current:
        time_entry = instance.get_current_entry()
        logger.info(time_entry)

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
            workspace = user_data.find_workspace(args.workspace)
            project = user_data.find_user_project(args.project)
            time_entry = time_entry_builder.TimeEntryBuilder.from_now(
                workspace, project, args.description, args.tags.split(','))
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
                args.project,
                args.workspace)
        except ValueError:
            workspace = user_data.find_workspace(args.workspace)
            project = project_builder.ProjectBuilder.from_name_and_workspace(
                args.name, workspace)
            instance.create_project(project)

    if args.list_workspaces:
        logger.info("\n{}".format(tabulate(
            [s.__str__().split(',') for s in user_data.workspaces],
            headers=["name", "id"],
            tablefmt="grid"
        )))

    if args.list_projects:
        logger.info("\n{}".format(tabulate(
            [s.__str__().split(',') for s in user_data.projects],
            headers=["name","workspace","id","color","hex"],
            tablefmt="grid"
        )))

    if args.list_tags:
        logger.info("\n{}".format(tabulate(
            [s.__str__().split(',') for s in user_data.tags],
            headers=["name", "workspace", "id"],
            tablefmt="grid"
        )))

    if args.list_time_entries:
        logger.info("\n{}".format(tabulate(
            [s.__str__().split(',') for s in user_data.time_entries],
            headers=["description", "id", "project", "workspace", "duration"],
            tablefmt="grid"
        )))
