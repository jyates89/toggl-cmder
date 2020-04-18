import click
from tabulate import tabulate
import logging
from typing import List

from togglcmder.toggl.cli.workspaces \
    import sync_or_retrieve_workspaces, retrieve_workspace_from_context

from togglcmder.toggl.cli.helpers import retrieve_cache_from_context
from togglcmder.toggl.cli.helpers import retrieve_commands_from_context
from togglcmder.toggl.cli.helpers import retrieve_downloader_from_context

from togglcmder.toggl.caching import Caching
from togglcmder.toggl.commands import Commands

from togglcmder.toggl.types.workspace import Workspace
from togglcmder.toggl.filters.workspaces import Workspaces as WorkspaceFilter

from togglcmder.toggl.types.tag import Tag
from togglcmder.toggl.builders.tag_builder import TagBuilder
from togglcmder.toggl.views.tag import Tag as TagView
from togglcmder.toggl.filters.tags import Tags as TagFilter


def sync_or_retrieve_tags(context_obj: dict, workspace: Workspace) -> List[Tag]:
    caching = retrieve_cache_from_context(context_obj)
    downloader = retrieve_downloader_from_context(context_obj)

    # Download any new tags if remote sync is enabled.
    if context_obj['sync'] is True:
        current_tags = downloader.download_tags(workspace)
        if current_tags:
            caching.update_tag_cache(current_tags)
    else:
        # Otherwise we just pull from the local cache.
        current_tags = caching.retrieve_tag_cache()

        if current_tags:
            # Retrieval from the DB doesn't filter on workspace, so we do that ourselves.
            current_tags = TagFilter.filter_on_workspace(current_tags, workspace)

    return current_tags


@click.group(
    help='Add, update, delete, and list tags.'
)
@click.option('--workspace')
@click.pass_context
def tags(context: click.Context, workspace: str):
    workspace_name = workspace or context.obj['config']['default_workspace']

    workspaces = sync_or_retrieve_workspaces(context.obj)

    if workspace_name:
        workspaces = WorkspaceFilter.filter_on_name(
            workspaces,
            workspace_name
        )

        workspaces_found = len(workspaces)
        if workspaces_found == 1:
            context.obj['data']['workspace'] = workspaces[0]

    context.obj['data']['workspaces'] = workspaces

    current_tags = []
    for current_workspace in workspaces:
        synced_tags = sync_or_retrieve_tags(context.obj, current_workspace)
        if synced_tags:
            current_tags.extend(synced_tags)

    context.obj['data']['tags'] = current_tags


@tags.command('add')
@click.option('--name',
              required=True)
@click.pass_context
def tag_add(context: click.Context, name: str):
    workspace = retrieve_workspace_from_context(context.obj)
    if not workspace:
        # Workspace required to add a new tag.
        click.echo(click.style('ERROR', fg='red') +
                   ': a workspace is required when adding a new tag.')
        return

    current_tags = context.obj['data']['tags']
    if current_tags:
        current_tags = TagFilter.filter_on_name(
            current_tags, name)
        if current_tags:
            click.echo(click.style('WARNING', fg='yellow') +
                       f': tag({name}) with this name already'
                       f' exists in this workspace({workspace.name}).')
            return

    tag = TagBuilder()\
        .name(name)\
        .workspace_identifier(workspace.identifier)\
        .build()

    cache = retrieve_cache_from_context(context.obj)
    commands = retrieve_commands_from_context(context.obj)

    # This raises if there is any issues, which means it doesn't get added
    # to the local cache.
    try:
        added_tag = commands.add_tag(tag)

        # The new tag was added to the remote Toggl servers, so now
        # we can add it to our local cache as well.
        cache.update_tag_cache([added_tag])
        click.echo(click.style('SUCCESS', fg='green') +
                   f': added new tag({added_tag.name}) to'
                   f' workspace({workspace.name})!')

    except Exception as e:
        logging.getLogger(__name__).error(e)
        click.echo(click.style('ERROR', fg='red') +
                   f': failed to add new tag({name}) to workspace({workspace.name}).'
                   ' An exception has been logged; check the logs for more information.')


@tags.command('delete')
@click.option('--name')
@click.option('--multiple',
              is_flag=True,
              default=False,
              show_default=True)
@click.pass_context
def tag_delete(context: click.Context, name: str, multiple: bool):
    workspace = retrieve_workspace_from_context(context.obj)
    if not workspace:
        # Workspace filter was not strict enough or there is no default
        # workspace configured.
        click.echo(click.style('ERROR', fg='red') +
                   ': a single workspace must be specified (default or otherwise'
                   ' ) when deleting a tag.')
        return

    current_tags = context.obj['data']['tags']

    if not current_tags:
        click.echo(click.style('WARNING') +
                   f': there are no tags in this workspace({workspace.name}).')
        return

    if name:
        current_tags = TagFilter.filter_on_name(
            current_tags, name
        )
        if not current_tags:
            click.echo(click.style('WARNING', fg='yellow') +
                       f': no tags exist with this name({name}'
                       f' in this workspace({workspace.name})')
            return

    if not multiple and len(current_tags) > 1:
        click.echo(click.style('ERROR', fg='red') +
                   ': multiple tags found matching the criteria, but --multiple '
                   'not specified.. please use the --multiple option or tighten '
                   'the search criteria.')
        return

    cache = retrieve_cache_from_context(context.obj)
    commands = retrieve_commands_from_context(context.obj)

    # This raises if there is any issues, which means it doesn't get added
    # to the local cache.
    try:
        for tag in current_tags:
            commands.delete_tag(tag)

            # The new tag was removed from the remote Toggl servers, so now
            # we can remove it from our local cache as well.
            cache.remove_tag_from_cache(tag)
            click.echo(click.style('SUCCESS', fg='green') +
                       f': deleted tag({tag.name})!')

    except Exception as e:
        logging.getLogger(__name__).error(e)
        click.echo(click.style('ERROR', fg='red') +
                   f': failed to delete the tag(s). An exception has been logged;'
                   ' check the logs for more information.')


@tags.command('update')
@click.option('--old-name',
              required=True)
@click.option('--new-name',
              required=True)
@click.pass_context
def tag_update(context: click.Context, old_name: str, new_name: str):
    workspace = retrieve_workspace_from_context(context.obj)
    if not workspace:
        # Workspace filter was not strict enough or there is no default
        # workspace configured.
        click.echo(click.style('ERROR', fg='red') +
                   ': a single workspace must be specified (default or otherwise'
                   ' ) when updating a tag.')
        return

    current_tags = context.obj['data']['tags']
    if not current_tags:
        click.echo(click.style('WARNING', fg='yellow') +
                   f': no tags to update in this workspace({workspace.name}).')
        return

    current_tags = TagFilter.filter_on_name(current_tags, old_name)
    if not current_tags:
        click.echo(click.style('WARNING', fg='yellow') +
                   f': no tags with name({old_name}) found in this workspace({workspace.name}).')
        return
    elif len(current_tags) > 1:
        click.echo(click.style('ERROR', fg='red') +
                   f': multiple tags found matching name({old_name}), in'
                   f' this workspace({workspace.name}).. please be more specific.')
        return

    # Only support updating a single tag at a time, because updating multiple tags
    # at once doesn't make sense when the only thing you can update is the name.
    builder = TagBuilder(current_tags[0])
    builder.name(new_name)
    updated_tag = builder.build()

    cache = context.obj['cache']
    assert(isinstance(cache, Caching))

    commands = context.obj['commands']
    assert(isinstance(commands, Commands))

    try:
        updated_tag = commands.update_tag(updated_tag)
        cache.update_tag_cache([updated_tag])
        click.echo(click.style('SUCCESS', fg='green') +
                   f': updated tag({old_name}) to tag({new_name})!')

    except Exception as e:
        logging.getLogger(__name__).error(e)
        click.echo(click.style('ERROR', fg='red') +
                   f': failed to update the tags. An exception has been logged;'
                   ' check the logs for more information.')


@tags.command('list')
@click.option('--name')
@click.option('--sort-by',
              type=click.Choice([val.__str__() for val in TagView.headers()]),
              default=TagView.headers()[0],
              show_default=True)
@click.pass_context
def tag_list(context: click.Context, name: str, sort_by: str):
    workspaces = context.obj['data']['workspaces']
    current_tags = context.obj['data']['tags']
    if not current_tags:
        click.echo(click.style('WARNING', fg='yellow') +
                   f': no tags found in the specified workspace(s).')
        return

    if name:
        current_tags = TagFilter.filter_on_name(
            current_tags, name
        )
        if not current_tags:
            click.echo(click.style('WARNING', fg='yellow') +
                       f': no tags found with name({name}).')
            return

    rows = []
    for current_workspace in workspaces:
        filtered_tags = TagFilter.filter_on_workspace(
            current_tags, current_workspace
        )
        if filtered_tags:
            rows.extend(
                TagView(
                    tags=filtered_tags,
                    workspace=current_workspace
                ).values()
            )

    sort_by_index = 0
    if sort_by:
        if sort_by not in TagView.headers():
            click.echo(f'Choose a valid header to sort by: {TagView.headers()}')
            return
        for index, header in enumerate(TagView.headers()):
            if sort_by == header:
                sort_by_index = index
                break

    rows = sorted(rows, key=lambda key: key[sort_by_index], reverse=True)
    click.echo_via_pager(tabulate(
        rows,
        headers=TagView.headers(),
        tablefmt="grid"
    ))
