#!/usr/bin/env python

import os
import click
import json
import logging
import logging.handlers
import sys

from typing import Optional, List

from togglcmder.version import __version__

from togglcmder.toggl.cli.workspaces import workspaces as workspace_cli
from togglcmder.toggl.cli.projects import projects as project_cli
from togglcmder.toggl.cli.tags import tags as tag_cli
from togglcmder.toggl.cli.time_entries import timers as timer_cli

from togglcmder.toggl.caching import Caching
from togglcmder.toggl.downloader import Downloader
from togglcmder.toggl.commands import Commands


@click.group(invoke_without_command=True)
@click.option(
    '--api-key',
    help='Your API key for the Toggl API',
    type=str,
    show_envvar=True,
    allow_from_autoenv=True
)
@click.option(
    '--reset-api-key',
    help='Resets the Toggl API key and downloads it to the local device.',
    is_flag=True,
    flag_value=True,
    callback=lambda c, x, v: click.confirm('Are you sure you want to reset the API key?') if v else False
)
@click.option(
    '--default-workspace',
    help='Specify a default workspace to use when otherwise not specified.',
    show_envvar=True,
    allow_from_autoenv=True
)
@click.option(
    '--default-project',
    help='Specify a default project to use when otherwise not specified.',
    show_envvar=True,
    allow_from_autoenv=True
)
@click.option(
    '--default-tags',
    help='Specify some default tags to always include for timers started on this machine.',
    show_envvar=True,
    allow_from_autoenv=True
)
@click.option(
    '--default-time-entry-start-days',
    help='Specify some default start time to refresh time entries.',
    type=int
    # help='This is the number of days before now we should start looking for time '
    #     'entries when doing a refresh. The default of "30" means look for '
    #     'time entries starting from 30 days ago.'
)
@click.option(
    '--default-time-entry-stop-days',
    help='Specify some default stop time to refresh time entries.',
    type=int
    # help='This is the number of days before now that we should stop looking '
    #     'for time entries when doing a refresh. The default of "0" means'
    #     'make the stop time now.'
)
@click.option(
    '--verbosity', '-v',
    default=0,
    count=True
)
@click.option(
    '--version',
    is_flag=True,
    callback=lambda c, t, v: click.echo(f"Version {__version__}") & c.exit() if v else False,
    expose_value=False,
    is_eager=True
)
@click.option(
    '--sync',
    help='Download from remote Toggl servers before attempting item lookups.',
    is_flag=True,
    default=False,
    show_default=True
)
@click.option(
    '--show-config',
    help='Simply prints the current configuration.',
    is_flag=True,
    default=False
)
@click.pass_context
def main(context: click.Context,
         api_key: str,
         reset_api_key: bool,
         default_workspace: str,
         default_project: str,
         default_tags: str,
         default_time_entry_start_days: int,
         default_time_entry_stop_days: int,
         verbosity: int,
         sync: bool,
         show_config: bool):

    # This object (context object provided by Click for sharing data between the
    # various command chains) contains configuration, defaults, and the objects we
    # create in the entry point to establish a connection to the database and start
    # logging to the file. The data key contains the current relevant objects, such
    # as workspaces, projects, tags, or time entries.
    context.obj = {
        'config': {
            'api_key': Optional[str],
            'default_workspace': Optional[str],
            'default_project': Optional[str],
            'default_tags': Optional[List[str]],
            'default_time_entry_window_start_days': 5,
            'default_time_entry_window_stop_days': 0
        },
        'cache': Optional[Caching],
        'downloader': Optional[Downloader],
        'commands': Optional[Commands],
        'sync': sync,
        'data': {
            'workspaces': [],
            'workspace': None,
            'projects': [],
            'project': None,
            'tags': [],
            'time_entries': []
        }
    }
    context.obj['config']['api_key'] = None
    context.obj['config']['default_workspace'] = 'Everything'
    context.obj['config']['default_project'] = None
    context.obj['config']['default_tags'] = None

    # Set up the paths paths that we need.
    app_dir = click.get_app_dir('togglcmder')

    # Configuration file is automatically created and stored in the application
    # directory for the user. If it exists, it's simply loaded.
    config = os.path.join(app_dir, 'toggl.json')
    if not os.path.exists(app_dir):
        os.mkdir(app_dir)

    if not os.path.exists(config):
        with open(config, 'w') as handle:
            json.dump(context.obj['config'], handle, sort_keys=True, indent=4)
    else:
        with open(config, 'r') as handle:
            # Merge the defaults in with the actual configuration.
            context.obj['config'] = {**context.obj['config'], **json.load(handle)}

    # If the user provides the API key, we overwrite the key from the configuration
    # file and use that for all future requests.
    if not api_key and not context.obj['config']['api_key']:
        click.echo(click.style('ERROR', fg='red', bold=True) +
                   ': there is no API key yet.. please insert the key into'
                   f' {config} or provide it with the "--api-key" argument!')
        return

    logger = logging.getLogger()

    # Logs to the app directory instead of where the script is run from.
    log_path = os.path.join(app_dir, 'toggl.log')
    log_file_handle = logging.handlers.RotatingFileHandler(log_path)

    # TODO: is this formatted string sufficient for logging? Too much?
    formatter = logging.Formatter(
        "%(asctime)s: %(levelname)s: %(name)s: %(lineno)d: %(message)s",
        "%Y-%m-%dT%H:%M:%S")

    log_file_handle.setFormatter(formatter)

    logger.addHandler(log_file_handle)

    # The way logger handles the debug levels is a bit odd, so we need to do
    # this to allow the the user to change the levels as expected. e.g. -vvv
    # allows more verbosity than just -v.
    logger.setLevel(60 - ((3 + verbosity) * 10))

    cache = Caching(cache_name=os.path.join(app_dir, 'cache.db'))
    context.obj['cache'] = cache

    if api_key:
        context.obj['config']['api_key'] = api_key

    # We obviously cannot do anything without an API key.
    if not context.obj['config']['api_key']:
        click.echo(click.style("ERROR", fg="red") +
                   ": there is no API key defined. Check the README or Wiki for "
                   "more information.")
        return

    # The API key can be reset and is automatically updated in both the file and
    # the running instance of the script.
    if reset_api_key:
        try:
            context.obj['config']['api_key'] = Commands(
                context.obj['config']['api_key']).reset_api_token().strip('"')
            click.echo(click.style("SUCCESS", fg="green") +
                       "API key successfully reset!")
        except Exception as e:
            click.echo(click.style("ERROR", fg="red") +
                       "Failed to reset API key. Check logs for more information.")
            logger.error(e)

    # These defaults can allow users to start timers without needing to specify
    # a workspace and project every single time. If the specific options for a
    # given command are not provided then these are used.
    if default_workspace:
        if default_workspace == 'None':
            context.obj['config']['default_workspace'] = None
        else:
            context.obj['config']['default_workspace'] = default_workspace

    if default_project:
        if default_project == 'None':
            context.obj['config']['default_project'] = None
        else:
            context.obj['config']['default_project'] = default_project

    if default_tags:
        if default_tags == 'None':
            context.obj['config']['default_tags'] = None
        else:
            context.obj['config']['default_tags'] = [t.strip() for t in default_tags.split(',')]

    if default_time_entry_start_days:
        context.obj['config']['default_time_entry_window_start_days'] = default_time_entry_start_days

    if default_time_entry_stop_days:
        context.obj['config']['default_time_entry_window_stop_days'] = default_time_entry_stop_days

    # We've updated the configuration internally, now update it on disk.
    with open(config, 'w') as handle:
        json.dump(context.obj['config'], handle, sort_keys=True, indent=4)

    if show_config:
        click.echo(context.obj['config'])

    # Set up the command and downloader objects with the API key.
    context.obj['commands'] = Commands(context.obj['config']['api_key'])
    context.obj['downloader'] = Downloader(context.obj['config']['api_key'])


######################################################


assert(isinstance(main, click.Group))

main.add_command(workspace_cli)
main.add_command(project_cli)
main.add_command(tag_cli)
main.add_command(timer_cli)

######################################################

if __name__ == "__main__":
    main(auto_envvar_prefix='TOGGL')
