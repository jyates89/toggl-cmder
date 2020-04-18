import click
from tabulate import tabulate
import logging
from typing import List, Optional

from togglcmder.toggl.cli.workspaces \
    import sync_or_retrieve_workspaces, retrieve_workspace_from_context

from togglcmder.toggl.cli.helpers import retrieve_cache_from_context
from togglcmder.toggl.cli.helpers import retrieve_commands_from_context
from togglcmder.toggl.cli.helpers import retrieve_downloader_from_context

from togglcmder.toggl.types.workspace import Workspace
from togglcmder.toggl.filters.workspaces import Workspaces as WorkspaceFilter

from togglcmder.toggl.types.project import Project
from togglcmder.toggl.builders.project_builder import ProjectBuilder
from togglcmder.toggl.views.project import Project as ProjectView
from togglcmder.toggl.filters.projects import Projects as ProjectFilter


def sync_or_retrieve_projects(context_obj: dict, workspace: Workspace) -> List[Project]:
    caching = retrieve_cache_from_context(context_obj)
    downloader = retrieve_downloader_from_context(context_obj)

    # Download any new projects if remote sync is enabled.
    if context_obj['sync'] is True:
        current_projects = downloader.download_projects(workspace)
        if current_projects:
            caching.update_project_cache(current_projects)
    else:
        # Otherwise we just pull from the local cache.
        current_projects = caching.retrieve_project_cache()

        if current_projects:
            # Retrieval from DB doesn't filter on workspace, so we do that ourselves.
            current_projects = ProjectFilter.filter_on_workspace(current_projects, workspace)

    return current_projects


def retrieve_project_from_context(context: dict) -> Optional[Project]:
    project = context['data']['project']
    return project


@click.group(
    help='Add, update, delete, and list projects.'
)
@click.option('--workspace')
@click.pass_context
def projects(context: click.Context, workspace: str):
    workspace_name = workspace or context.obj['config']['default_workspace']

    workspaces = sync_or_retrieve_workspaces(context.obj)

    if workspace_name:
        workspaces = WorkspaceFilter.filter_on_name(
            workspaces,
            workspace_name)

        workspaces_found = len(workspaces)
        if workspaces_found == 1:
            context.obj['data']['workspace'] = workspaces[0]

    context.obj['data']['workspaces'] = workspaces

    current_projects = []
    for current_workspace in workspaces:
        synced_projects = sync_or_retrieve_projects(context.obj, current_workspace)
        if synced_projects:
            current_projects.extend(synced_projects)

    context.obj['data']['projects'] = current_projects


@projects.command('add')
@click.option('--name',
              required=True)
@click.option('--color',
              type=click.Choice([val.__str__() for val in Project.Color]),
              default=Project.Color.BLACK.name.lower())
@click.pass_context
def project_add(context: click.Context, name: str, color: str):
    workspace = retrieve_workspace_from_context(context.obj)
    if not workspace:
        # Workspace filter was not strict enough or there is no default
        # workspace configured.
        click.echo(click.style('ERROR', fg='red') +
                   ': a single workspace must be specified (default or otherwise'
                   ' ) when adding a new project.')
        return

    # If there is a project with the same name existing already, do nothing.
    current_projects = context.obj['data']['projects']
    if current_projects:
        current_projects = ProjectFilter.filter_on_name(
            current_projects, name)
        if current_projects:
            click.echo(click.style('WARNING', fg='yellow') +
                       f': project({name}) with this name already'
                       f' exists in this workspace({workspace.name}).')
            return

    project = ProjectBuilder() \
        .name(name) \
        .workspace_identifier(workspace.identifier) \
        .color(Project.Color.from_string(color)) \
        .build()

    commands = retrieve_commands_from_context(context.obj)
    cache = retrieve_cache_from_context(context.obj)

    # This raises if there is any issues, which means it doesn't get added
    # to the local cache.
    try:
        added_project = commands.add_project(project)
        # The new project was added to the remote Toggl servers, so now
        # we can add it to our local cache as well.
        cache.update_project_cache([added_project])

        click.echo(click.style('SUCCESS', fg='green') +
                   f': added new project({added_project.name}) to'
                   f' workspace({workspace.name})!')

    except Exception as e:
        logging.getLogger(__name__).error(e)
        click.echo(click.style('ERROR', fg='red') +
                   f': failed to add new project({name}) to workspace({workspace.name}).'
                   ' An exception has been logged; check the logs for more information.')


@projects.command('delete')
@click.option('--name')
@click.option('--color',
              type=click.Choice([val.__str__() for val in Project.Color]))
@click.option('--multiple',
              is_flag=True,
              default=False,
              show_default=True)
@click.pass_context
def project_delete(context: click.Context, name: str, color: str,
                   multiple: bool):
    workspace = retrieve_workspace_from_context(context.obj)
    if not workspace:
        # Workspace filter was not strict enough or there is no default
        # workspace configured.
        click.echo(click.style('ERROR', fg='red') +
                   ': a single workspace must be specified (default or otherwise'
                   ' ) when deleting a project.')
        return

    current_projects = context.obj['data']['projects']
    if not current_projects:
        click.echo(click.style('WARNING', fg='yellow') +
                   f': no projects exist in this workspace({workspace.name})!')
        return

    if color:
        # See if the user specified a color to search on.
        current_projects = ProjectFilter.filter_on_color(
            current_projects, Project.Color.from_string(color))
        if not current_projects:
            click.echo(click.style('WARNING', fg='yellow') +
                       f': no projects exist with this color({color})'
                       f' in this workspace({workspace.name}).')
            return

    if name:
        current_projects = ProjectFilter.filter_on_name(
            current_projects, name)
        if not current_projects:
            click.echo(click.style('WARNING', fg='yellow') +
                       f': no projects exist with this name({name}'
                       f' in this workspace({workspace.name}).')
            return

    if not multiple and len(current_projects) > 1:
        # If multiple matches are found but the user didn't specify the --multiple option,
        # prevent accidental deletion by requiring the user do it again but with the option
        # enabled.
        click.echo(click.style('ERROR', fg='red') +
                   ': multiple projects found matching the criteria, but --multiple '
                   'not specified.. please use the --multiple option or tighten '
                   'the search criteria.')
        return

    commands = retrieve_commands_from_context(context.obj)
    cache = retrieve_cache_from_context(context.obj)

    try:
        if len(current_projects) > 1:
            commands.delete_projects(current_projects)
            for project in current_projects:
                cache.remove_project_from_cache(project)
                click.echo(click.style('SUCCESS', fg='green') +
                           f': deleted project({project.name})!')
        else:
            commands.delete_project(current_projects[0])
            cache.remove_project_from_cache(current_projects[0])
            click.echo(click.style('SUCCESS', fg='green') +
                       f': deleted project({current_projects[0].name})!')

    except Exception as e:
        logging.getLogger(__name__).error(e)
        click.echo(click.style('ERROR', fg='red') +
                   f': failed to delete the project(s). An exception has been logged;'
                   ' check the logs for more information.')


@projects.command('update')
@click.option('--old-name')
@click.option('--old-color',
              type=click.Choice([val.__str__() for val in Project.Color]))
@click.option('--new-name')
@click.option('--new-color',
              type=click.Choice([val.__str__() for val in Project.Color]))
@click.option('--multiple',
              is_flag=True,
              default=False,
              show_default=True)
@click.pass_context
def project_update(context: click.Context, old_name: str, old_color: str,
                   new_name: str, new_color: str, multiple: bool):
    workspace = retrieve_workspace_from_context(context.obj)
    if not workspace:
        # Workspace filter was not strict enough or there is no default
        # workspace configured.
        click.echo(click.style('ERROR', fg='red') +
                   ': a single workspace must be specified (default or otherwise'
                   ' ) when updating a project.')
        return

    current_projects = context.obj['data']['projects']
    if not current_projects:
        click.echo(click.style('WARNING', fg='yellow') +
                   f': no projects to update in this workspace({workspace.name}).')
        return

    if old_color:
        # See if the user specified a color to search on.
        current_projects = ProjectFilter.filter_on_color(
            current_projects, Project.Color.from_string(old_color))
        if not current_projects:
            click.echo(click.style('WARNING', fg='yellow') +
                       f': no projects exist with this color({old_color})'
                       f' in this workspace({workspace.name}).')
            return

    if old_name:
        current_projects = ProjectFilter.filter_on_name(
            current_projects, old_name)
        if not current_projects:
            click.echo(click.style('WARNING', fg='yellow') +
                       f': no projects exist with this name({old_name}'
                       f' in this workspace({workspace.name}).')
            return

    if not multiple and len(current_projects) > 1:
        click.echo(click.style('ERROR', fg='red') +
                   ': multiple projects found matching the criteria, but --multiple '
                   'not specified.. please used the --multiple option or tighten '
                   'the search criteria.')
        return

    current_builds: List[ProjectBuilder] = []
    for project in current_projects:
        current_builds.append(
            ProjectBuilder(project))

    if new_name:
        for build in current_builds:
            assert isinstance(build, ProjectBuilder)
            build.name(new_name)
    if new_color:
        for build in current_builds:
            assert isinstance(build, ProjectBuilder)
            build.color(Project.Color.from_string(new_color))

    cache = retrieve_cache_from_context(context.obj)
    commands = retrieve_commands_from_context(context.obj)

    try:
        built_projects = []
        for project_builder in current_builds:
            project = project_builder.build()
            project = commands.update_project(project)
            click.echo(click.style('SUCCESS', fg='green') +
                       f': updated project({project.name}) in'
                       f' workspace({workspace.name}).')
            built_projects.append(project)
        cache.update_project_cache(built_projects)

    except Exception as e:
        logging.getLogger(__name__).error(e)
        click.echo(click.style('ERROR', fg='red') +
                   f': failed to update the project(s). An exception has been logged;'
                   ' check the logs for more information.')


@projects.command('list')
@click.option('--name')
@click.option('--color',
              type=click.Choice([val.__str__() for val in Project.Color]))
@click.option('--sort-by',
              type=click.Choice([val.__str__() for val in ProjectView.headers()]),
              default=ProjectView.headers()[0],
              show_default=True)
@click.pass_context
def project_list(context: click.Context, name: str, color: str, sort_by: str):
    # Workspaces are already filtered if needed, otherwise this will
    # show all projects in all workspaces.
    workspaces = context.obj['data']['workspaces']

    # Projects are already filtered for any specified workspace.
    current_projects = context.obj['data']['projects']
    if not current_projects:
        click.echo(click.style('WARNING', fg='yellow') +
                   f': no projects found in the specified workspace(s).')
        return

    if name:
        current_projects = ProjectFilter.filter_on_name(
            current_projects, name)
        if not current_projects:
            click.echo(click.style('WARNING', fg='yellow') +
                       f': no projects exist with this name({name}).')
            return

    if color:
        # See if the user specified a color to search on.
        current_projects = ProjectFilter.filter_on_color(
            current_projects, Project.Color.from_string(color))
        if not current_projects:
            click.echo(click.style('WARNING', fg='yellow') +
                       f': no projects exist with this color({color}).')
            return

    rows = []
    for current_workspace in workspaces:
        filtered_projects = ProjectFilter.filter_on_workspace(
            current_projects, current_workspace)
        if filtered_projects:
            rows.extend(
                ProjectView(
                    projects=filtered_projects,
                    workspace=current_workspace
                ).values()
            )

    sort_by_index = 0
    if sort_by:
        for index, header in enumerate(ProjectView.headers()):
            if sort_by == header:
                sort_by_index = index
                break

    rows = sorted(rows, key=lambda key: key[sort_by_index], reverse=True)
    click.echo_via_pager(tabulate(
        rows,
        headers=ProjectView.headers(),
        tablefmt="grid"))
