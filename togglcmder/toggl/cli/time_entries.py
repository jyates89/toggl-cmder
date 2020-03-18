import re
import click
from tabulate import tabulate
import logging
from typing import List, Optional
from requests.exceptions import HTTPError
import functools

from datetime import datetime, timedelta
from tzlocal import get_localzone

from togglcmder.toggl.cli.workspaces \
    import sync_or_retrieve_workspaces, retrieve_workspace_from_context

from togglcmder.toggl.cli.projects \
    import sync_or_retrieve_projects, retrieve_project_from_context

from togglcmder.toggl.cli.tags import sync_or_retrieve_tags

from togglcmder.toggl.cli.helpers import retrieve_cache_from_context
from togglcmder.toggl.cli.helpers import retrieve_commands_from_context
from togglcmder.toggl.cli.helpers import retrieve_downloader_from_context

from togglcmder.toggl.types.workspace import Workspace
from togglcmder.toggl.filters.workspaces import Workspaces as WorkspaceFilter

from togglcmder.toggl.types.project import Project
from togglcmder.toggl.filters.projects import Projects as ProjectFilter

from togglcmder.toggl.types.tag import Tag
from togglcmder.toggl.filters.tags import Tags as TagFilter

from togglcmder.toggl.types.time_entry import TimeEntry
from togglcmder.toggl.builders.time_entry_builder import TimeEntryBuilder
from togglcmder.toggl.views.time_entry import TimeEntry as TimeEntryView
from togglcmder.toggl.filters.time_entries import TimeEntries as TimeEntryFilter


def validated_time(date_time: str) -> datetime:
    result = re.match(r'^now(?P<value>[+-]\d+)?(?P<unit>[ydhms])?$',
                      date_time)
    if result is not None:
        now = get_localzone().localize(datetime.now())
        value = result.group('value')
        if not value:
            return now
        if result.group('unit') == 'd':
            return now + timedelta(days=float(value))
        elif result.group('unit') == 'h':
            return now + timedelta(hours=float(value))
        elif result.group('unit') == 'm':
            return now + timedelta(minutes=float(value))
        elif result.group('unit') == 's':
            return now + timedelta(seconds=float(value))

    try:
        return get_localzone().localize(datetime.fromisoformat(date_time))
    except ValueError:
        raise RuntimeError(f"Not a valid time: '{date_time}'.")


def sync_or_retrieve_time_entries(context_obj: dict, workspace: Workspace, start: datetime, stop: datetime, *,
                                  project: Optional[Project] = None) -> List[TimeEntry]:
    caching = retrieve_cache_from_context(context_obj)
    downloader = retrieve_downloader_from_context(context_obj)

    # Download any new time entries if remote sync is enabled.
    if context_obj['sync'] is True:
        current_time_entries = downloader.download_time_entries(start, stop)
        if current_time_entries:
            caching.update_time_entry_cache(current_time_entries)
    else:
        # Otherwise we just pull from the local cache.
        current_time_entries = caching.retrieve_time_entry_cache()

    # Neither downloading from remote nor pulling from local cache does any filtering, so let's do that.
    current_time_entries = TimeEntryFilter.filter_on_workspace(current_time_entries, workspace)

    # It also doesn't filter on start/stop, so let's do that too.
    current_time_entries = TimeEntryFilter.filter_on_date_range(current_time_entries, start, stop)

    # Time entries _can_ be filtered on project if it is provided.
    current_time_entries = TimeEntryFilter.filter_on_project(current_time_entries, project)

    return current_time_entries


@click.group(
    help='Add, update, delete, start, stop, and list timers.'
)
@click.option('--workspace')
@click.option('--project')
@click.option('--download-start',
              type=validated_time,
              help='This can be now[-/+[dhms]] or an iso formatted time string.')
@click.option('--download-stop',
              type=validated_time,
              help='This can be now[-/+[dhms]] or an iso formatted time string.')
@click.pass_context
def timers(context: click.Context,
           workspace: str,
           project: str,
           download_start: datetime,
           download_stop: datetime):
    workspace_name = workspace or context.obj['config']['default_workspace']
    project_name = project or context.obj['config']['default_project']

    workspaces = sync_or_retrieve_workspaces(context.obj)
    if workspace_name:
        # If a workspace name is provided, default or otherwise, filter on it.
        workspaces = WorkspaceFilter.filter_on_name(
            workspaces,
            workspace_name)

        # If a single workspace was found we can store it.
        workspaces_found = len(workspaces)
        if workspaces_found == 1:
            context.obj['data']['workspace'] = workspaces[0]

    context.obj['data']['workspaces'] = workspaces

    projects = []
    # Whether or not we have workspaces filtered, we can download all projects.
    for current_workspace in workspaces:
        synced_projects = sync_or_retrieve_projects(context.obj, current_workspace)
        if synced_projects:
            projects.extend(synced_projects)

    if project_name and not projects:
        # No projects exist in this workspace, but the user requested to filter on one.
        return

    if projects and project_name:
        # If there is a specified project name then we can filter on it.
        projects = ProjectFilter.filter_on_name(
            projects,
            project_name)

        # If a single project was found, we can store it too.
        projects_found = len(projects)
        if projects_found == 1:
            context.obj['data']['project'] = projects[0]
    context.obj['data']['projects'] = projects

    tags = []
    for current_workspace in workspaces:
        synced_tags = sync_or_retrieve_tags(context.obj, current_workspace)
        if synced_tags:
            tags.extend(synced_tags)
    context.obj['data']['tags'] = tags

    # Use our default window settings to download time entry updates.
    if not download_start:
        then = get_localzone().localize(
            datetime.now() - timedelta(days=context.obj['config']['default_time_entry_window_start_days']))
    else:
        then = download_start

    if not download_stop:
        now = get_localzone().localize(
            datetime.now() - timedelta(days=context.obj['config']['default_time_entry_window_stop_days']))
    else:
        now = download_stop

    time_entries = []
    for current_workspace in workspaces:
        for current_project in projects:
            if current_project.workspace_identifier == current_workspace.identifier:
                synced_entries = sync_or_retrieve_time_entries(
                    context.obj, current_workspace, then, now, project=current_project)
                if synced_entries:
                    time_entries.extend(synced_entries)
        if not projects:
            synced_entries = sync_or_retrieve_time_entries(
                context.obj, current_workspace, then, now)
            if synced_entries:
                time_entries.extend(synced_entries)

    context.obj['data']['time_entries'] = time_entries


@timers.command(
    'add',
    short_help='Add a completed time entry.',
    help='Add a new completed time entry. Stop time OR duration must be provided to add a valid '
         'completed entry.')
@click.option('--description')
@click.option('--start-time',
              type=validated_time,
              help='This can be now[-/+[dhms]] or an iso formatted time string.',
              required=True)
@click.option('--stop-time',
              type=validated_time,
              help='This can be now[-/+[dhms]] or an iso formatted time string.')
@click.option('--duration',
              help='The duration of this time entry. Stop time will be calculated if this is provided.',
              type=int)
@click.option('--tags')
@click.pass_context
def timer_add(context: click.Context,
              description: str,
              start_time: datetime,
              stop_time: datetime,
              duration: int,
              tags: str):
    workspace = retrieve_workspace_from_context(context)
    if not workspace:
        # Workspace filter was not strict enough or there is no default
        # workspace configured.
        click.echo(click.style('ERROR', fg='red') +
                   ': a single workspace must be specified (default or otherwise'
                   ' ) when adding a new timer.')
        return

    # Handling the error situations:
    if not stop_time and not duration:
        click.echo(click.style('ERROR', fg='red')
                   + ': you must specify a stop time or duration when adding a new timer.')
        return

    time_entries = context.obj['data']['time_entries']
    time_entries = TimeEntryFilter.filter_on_description(
        time_entries, description
    )

    if time_entries and description:
        click.echo(click.style('ERROR', fg='red')
                   + ': a timer with this description already exists.')
        return

    time_entry_builder = TimeEntryBuilder()
    time_entry_builder.workspace_identifier(workspace.identifier)

    project = retrieve_project_from_context(context)
    if project:
        time_entry_builder.project_identifier(project.identifier)

    if description:
        time_entry_builder.description(description)
    if start_time:
        time_entry_builder.start_time(dt=start_time)
    if stop_time:
        time_entry_builder.stop_time(dt=stop_time)
    if duration:
        time_entry_builder.duration(duration)
    elif stop_time:
        time_entry_builder.duration(
            int(stop_time.timestamp() - start_time.timestamp()))
    if tags:
        time_entry_builder.tags(tags.split(','))

    caching = retrieve_cache_from_context(context.obj)
    commands = retrieve_commands_from_context(context.obj)

    try:
        time_entry = time_entry_builder.build()
        time_entry = commands.add_completed_time_entry(time_entry)
        caching.update_time_entry_cache([time_entry])

        click.echo(click.style('SUCCESS', fg='green') +
                   f': added new time entry to'
                   f' workspace({workspace.name})!')

    except HTTPError as e:
        logging.getLogger(__name__).error(e)
        click.echo(click.style('ERROR', fg='red') +
                   f': failed to add new time entry to workspace({workspace.name}).'
                   ' An exception has been logged; check the logs for more information.')


@timers.command('delete')
@click.option('--description')
@click.option('--multiple',
              is_flag=True,
              default=False,
              show_default=True)
@click.option('--tags')
@click.pass_context
def timer_delete(context: click.Context, description: str, multiple: bool, tags: str):
    workspace = retrieve_workspace_from_context(context)
    if not workspace:
        # Workspace filter was not strict enough or there is no default
        # workspace configured.
        click.echo(click.style('ERROR', fg='red') +
                   ': a single workspace must be specified (default or otherwise'
                   ' ) when deleting a time entry.')
        return

    if not description and not tags:
        click.echo(click.style('ERROR', fg='red') +
                   f': either description or tags must be specified when deleting a timer.')
        return

    time_entries = context.obj['data']['time_entries']

    if description:
        time_entries = TimeEntryFilter.filter_on_description(
            time_entries, description
        )
        if not time_entries:
            click.echo(click.style('WARNING', fg='yellow') +
                       f': no time entries exist with the specified description.')
            return

    current_tags = context.obj['data']['tags']
    if tags:
        current_tags = TagFilter.filter_on_names(
            current_tags, tags.split(',')
        )
        if not current_tags:
            click.echo(click.style('WARNING', fg='yellow') +
                       f': no tags exist with the specified names.')
            return

        time_entries = TimeEntryFilter.filter_on_any_tags(
            time_entries, current_tags
        )
        if not time_entries:
            click.echo(click.style('WARNING', fg='yellow') +
                       f': no time entries exist with the specified tags.')
            return

    if len(time_entries) > 1 and not multiple:
        click.echo(click.style('ERROR', fg='red') +
                   ': multiple time entries found matching the criteria, but --multiple '
                   'not specified.. please use the --multiple option or tighten '
                   'the search criteria.')
        return

    caching = retrieve_cache_from_context(context.obj)
    commands = retrieve_commands_from_context(context.obj)

    try:
        for entry in time_entries:
            commands.delete_time_entry(entry)
            caching.remove_time_entry_from_cache(entry)
            click.echo(click.style('SUCCESS', fg='green') +
                       f': deleted timer({entry.description})!')

    except HTTPError as e:
        logging.getLogger(__name__).error(e)
        click.echo(click.style('ERROR', fg='red') +
                   f': failed to delete the timer(s). An exception has been logged;'
                   ' check the logs for more information.')


@timers.command('update',
                short_help='Update an existing time entry with new details.',
                help='Update an existing time entry with new details.')
@click.option('--old-description')
@click.option('--new-description')
@click.option('--new-project')
@click.option('--old-tags')
@click.option('--add-tags')
@click.option('--remove-tags')
@click.option('--new-start-time')
@click.option('--new-duration')
@click.option('--new-stop-time')
@click.option('--multiple',
              is_flag=True,
              default=False,
              show_default=True)
@click.pass_context
def timer_update(context: click.Context,
                 old_description: str,
                 new_description: str,
                 new_project: str,
                 old_tags: str,
                 add_tags: str,
                 remove_tags: str,
                 new_start_time: datetime,
                 new_duration: int,
                 new_stop_time: datetime,
                 multiple: bool):
    workspace = retrieve_workspace_from_context(context)
    if not workspace:
        # Workspace filter was not strict enough or there is no default
        # workspace configured.
        click.echo(click.style('ERROR', fg='red') +
                   ': a single workspace must be specified (default or otherwise'
                   ' ) when updating a timer.')
        return

    if not old_description or not old_tags:
        click.echo(click.style('ERROR', fg='red') +
                   f': either description or tags must be specified when deleting a timer.')
        return

    time_entries = context.obj['data']['time_entries']
    if not time_entries:
        click.echo(click.style('ERROR', fg='red') +
                   f': no time entries to update in this workspace({workspace.name}).')
        return

    if old_description:
        time_entries = TimeEntryFilter.filter_on_description(
            time_entries, old_description
        )
        if not time_entries:
            click.echo(click.style('WARNING', fg='yellow') +
                       f': no time entries exist with the specified description.')
            return

    current_tags = context.obj['data']['tags']
    if old_tags:
        current_tags = TagFilter.filter_on_names(
            current_tags, old_tags.split(',')
        )
        if not current_tags:
            click.echo(click.style('WARNING', fg='yellow') +
                       f': no tags exist with the specified names.')
            return

        time_entries = TimeEntryFilter.filter_on_any_tags(
            time_entries, current_tags
        )
        if not time_entries:
            click.echo(click.style('WARNING', fg='yellow') +
                       f': no time entries exist with the specified tags.')
            return
        # restore current_tags so we can filter it again if needed.
        current_tags = context.obj['data']['tags']

    if len(time_entries) > 1 and not multiple:
        click.echo(click.style('ERROR', fg='red') +
                   ': multiple timers found matching the criteria, but --multiple '
                   'not specified.. please used the --multiple option or tighten '
                   'the search criteria.')
        return

    projects = context.obj['data']['projects']
    new_specified_project: Optional[Project] = None
    if new_project:
        projects = ProjectFilter.filter_on_name(
            projects, new_project
        )
        if not projects:
            click.echo(click.style('ERROR', fg='red') +
                       f': no projects found with specified name.')
            return
        elif len(projects) > 1:
            click.echo(click.style('ERROR', fg='red') +
                       f': multiple projects found with specified name. Update criteria '
                       f' to match a single project.')
            return
        new_specified_project = projects[0]

    additional_tags: Optional[List[Tag]] = None
    if add_tags:
        current_tags = TagFilter.filter_on_names(
            current_tags, add_tags.split(',')
        )
        if not current_tags:
            click.echo(click.style('ERROR', fg='red') +
                       f': no tags found with the specified names in --add-tags.')
            return
        # restore current_tags so we can filter it again if needed.
        current_tags = context.obj['data']['tags']

    removed_tags: Optional[List[Tag]] = None
    if remove_tags:
        current_tags = TagFilter.filter_on_names(
            current_tags, remove_tags.split(',')
        )
        if not current_tags:
            click.echo(click.style('ERROR', fg='red') +
                       f': no tags found with the specified names in --remove-tags.')
            return

    entries: List[TimeEntry] = []
    for time_entry in time_entries:
        time_entry_builder = TimeEntryBuilder(time_entry)
        if new_description:
            time_entry_builder.description(new_description)
        if new_project:
            time_entry_builder.project_identifier(new_specified_project.identifier)
        if add_tags:
            time_entry_builder.add_tags([tag.name for tag in additional_tags])
        if remove_tags:
            time_entry_builder.remove_tags([tag.name for tag in removed_tags])
        if new_start_time:
            time_entry_builder.start_time(dt=new_start_time)
        if new_duration:
            time_entry_builder.duration(new_duration)
        if new_stop_time:
            time_entry_builder.stop_time(dt=new_stop_time)
        entries.append(time_entry_builder.build())

    caching = retrieve_cache_from_context(context.obj)
    commands = retrieve_commands_from_context(context.obj)

    try:
        updated_entries: List[TimeEntry] = []
        for entry in entries:
            updated_entry = commands.update_completed_time_entry(entry)
            updated_entries.append(updated_entry)
            click.echo(click.style('SUCCESS', fg='green') +
                       f': updated time entry({updated_entry.description}) in '
                       f' workspace({workspace.name})!')
        caching.update_time_entry_cache(updated_entries)

    except HTTPError as e:
        logging.getLogger(__name__).error(e)
        click.echo(click.style('ERROR', fg='red') +
                   f': failed to update the timer(s). An exception has been logged;'
                   ' check the logs for more information.')

@timers.command('start',
                short_help='Start a new running timer.',
                help='Start a new running timer. Has an implicit start time of '
                     'now. If no workspace or project is provided, defaults will '
                     'be used. If there are no defaults, an error will be issued.')
@click.option('--description')
@click.option('--tags')
@click.pass_context
def timer_start(context: click.Context, description: str, tags: str):
    time_entry_builder = TimeEntryBuilder()

    workspace = retrieve_workspace_from_context(context)
    if not workspace:
        # Workspace filter was not strict enough or there is no default
        # workspace configured.
        click.echo(click.style('ERROR', fg='red') +
                   ': a single workspace must be specified (default or otherwise'
                   ' ) when starting a timer.')
        return
    time_entry_builder.workspace_identifier(workspace.identifier)

    current_tags = context.obj['data']['tags']
    if tags:
        current_tags = TagFilter.filter_on_names(
            current_tags, tags.split(',')
        )
        if not current_tags:
            click.echo(click.style('ERROR', fg='red') +
                       f': no tags match the specified names.')
            return
        time_entry_builder.tags([tag.name for tag in current_tags])

    project = retrieve_project_from_context(context)
    if project:
        time_entry_builder.project_identifier(project.identifier)

    if description:
        time_entry_builder.description(description)

    time_entry_builder.start_time(dt=datetime.now(tz=get_localzone()))

    caching = retrieve_cache_from_context(context.obj)
    commands = retrieve_commands_from_context(context.obj)

    try:
        entry = time_entry_builder.build()
        entry = commands.start_time_entry(entry)
        click.echo(click.style('SUCCESS', fg='green') +
                   f': started new time entry({entry.description}) in'
                   f' workspace({workspace.name}).')
        caching.update_time_entry_cache([entry])

    except HTTPError as e:
        logging.getLogger(__name__).error(e)
        click.echo(click.style('ERROR', fg='red') +
                   f': failed to start the timer. An exception has been logged;'
                   ' check the logs for more information.')


@timers.command('stop',
                help='Stop the current running timer, if one exists.')
@click.pass_context
def timer_stop(context: click.Context):
    downloader = retrieve_downloader_from_context(context.obj)
    entry = downloader.get_current_time_entry()

    if not entry:
        click.echo('No entry is currently running.')
        return

    commands = retrieve_commands_from_context(context.obj)
    caching = retrieve_cache_from_context(context.obj)

    try:
        entry = commands.stop_time_entry(entry)
        caching.update_time_entry_cache([entry])
        click.echo(click.style('SUCCESS', fg='green') +
                   f': stopped the current running timer({entry.description}).')

    except HTTPError as e:
        logging.getLogger(__name__).error(e)
        click.echo(click.style('ERROR', fg='red') +
                   f': failed to stop the current running timer. An exception'
                   f' has been logged; check the logs for more information.')


@timers.command('current',
                help='Get the current running timer, if one exists.')
@click.pass_context
def timer_current(context: click.Context):
    project = retrieve_project_from_context(context)
    workspace = retrieve_workspace_from_context(context)

    downloader = retrieve_downloader_from_context(context.obj)

    try:
        entry = downloader.get_current_time_entry()
        if not entry:
            click.echo('No entry is currently running.')
        else:
            time_entry_view = TimeEntryView(
                [entry],
                project,
                workspace)
            click.echo_via_pager(tabulate(
                time_entry_view.values_sorted(),
                headers=TimeEntryView.headers(),
                tablefmt="grid"))

    except HTTPError as e:
        logging.getLogger(__name__).error(e)
        click.echo(click.style('ERROR', fg='red') +
                   f': failed to download the current running timer. An exception'
                   f' has been logged; check the logs for more information.')


@timers.command('resume',
                short_help='Resume the most recent timer.',
                help='Look through the list of timers, and resume the most recent one, '
                     'regardless of project or workspace.')
@click.pass_context
def timer_resume(context: click.Context):
    time_entries = context.obj['data']['time_entries']
    time_entries = sorted(time_entries, key=lambda entry: entry.last_updated,
                            reverse=True)

    commands = retrieve_commands_from_context(context.obj)
    caching = retrieve_cache_from_context(context.obj)

    try:
        time_entry_builder = TimeEntryBuilder(time_entries[0])
        time_entry_builder.start_time(dt=datetime.now(get_localzone()))
        time_entry_builder.unset_stop_time()
        time_entry_builder.unset_duration()
        started_entry = commands.start_time_entry(time_entry_builder.build())
        if started_entry:
            caching.update_time_entry_cache([started_entry])
        click.echo(click.style('SUCCESS', fg='green', bold=True) +
                   f': Resumed time entry({started_entry.description}).')
    except HTTPError as e:
        logging.getLogger(__name__).error(e)
        click.echo(click.style('ERROR', fg='red') +
                   f': failed to resume the latest timer. An exception'
                   f' has been logged; check the logs for more information.')


@timers.command('list')
@click.option('--description')
@click.option('--sort-by',
              type=click.Choice([val.__str__() for val in TimeEntryView.headers()]),
              default=TimeEntryView.headers()[5],
              show_default=True)
@click.pass_context
def timer_list(context: click.Context, description: str, sort_by: str):
    workspaces = context.obj['data']['workspaces']
    projects = context.obj['data']['projects']
    time_entries = context.obj['data']['time_entries']

    time_entries = TimeEntryFilter.filter_on_description(
        time_entries, description
    )
    if not time_entries:
        click.echo(click.style('WARNING', fg='yellow') +
                   f': no entries found in the specified workspace(s).')
        return

    rows = []
    for current_workspace in workspaces:
        reduced_entries = []
        # get all of the descriptions available
        descriptions = [entry.description for entry in time_entries]
        # remove any duplicates
        descriptions = list(dict.fromkeys(descriptions))
        for current_description in descriptions:
            # filter the actual entries on each unique description
            entries_on_description = TimeEntryFilter.filter_on_description(time_entries, current_description)
            # reduce down the entries with that description into a single entry
            combined_entry = functools.reduce(lambda x, y:
                                              TimeEntryBuilder(x).duration(x.duration + y.duration).build(),
                                              entries_on_description)
            reduced_entries.append(combined_entry)

        for entry in reduced_entries:
            project = ProjectFilter.filter_on_identifier(projects,
                                                         entry.project_identifier)
            rows.extend(
                TimeEntryView(
                    [entry], project[0] if project else None, current_workspace
                ).values()
            )

    # Sort by modified date by default.
    sort_by_index = 5
    if sort_by:
        if sort_by not in TimeEntryView.headers():
            click.echo(f'Choose a valid header to sort by: {TimeEntryView.headers()}')
            return
        for index, header in enumerate(TimeEntryView.headers()):
            if sort_by == header:
                sort_by_index = index
                break

    rows = sorted(rows, key=lambda key: key[sort_by_index], reverse=True)

    click.echo_via_pager(tabulate(
        rows,
        headers=TimeEntryView.headers(),
        tablefmt="grid"))
