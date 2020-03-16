import click
from tabulate import tabulate
from typing import List, Optional

from togglcmder.toggl.cli.helpers import retrieve_cache_from_context
from togglcmder.toggl.cli.helpers import retrieve_downloader_from_context

from togglcmder.toggl.types.workspace import Workspace
from togglcmder.toggl.views.workspace import Workspace as WorkspaceView


def sync_or_retrieve_workspaces(context_obj: dict) -> List[Workspace]:
    caching = retrieve_cache_from_context(context_obj)
    downloader = retrieve_downloader_from_context(context_obj)

    # Download any new workspaces added remotely (this is only possible via
    # the web interface anyway), if remote sync is enabled.
    if context_obj['sync'] is True:
        current_workspaces = downloader.download_workspaces()
        if current_workspaces:
            caching.update_workspace_cache(current_workspaces)
    else:
        # Otherwise we just pull from the local cache.
        current_workspaces = caching.retrieve_workspace_cache()

    return current_workspaces


def retrieve_workspace_from_context(context: click.Context) -> Optional[Workspace]:
    workspace = context.obj['data']['workspace']
    return workspace


@click.command(
    help='List the currently available workspaces.'
)
@click.pass_context
def workspaces(context: click.Context):
    current_workspaces = sync_or_retrieve_workspaces(context.obj)

    # This means the user is new and has not synced anything from the Toggl
    # servers. There is always at least one workspace called Everything!
    if not current_workspaces:
        click.echo(click.style('WARNING', fg='red') +
                   ': There are no workspaces available.')
        return

    # The only thing we can do with workspaces is list them,
    # so create the view and use the echo functionality click
    # provides so we aren't listing workspaces in the log.
    workspace_view = WorkspaceView(current_workspaces)
    click.echo_via_pager(tabulate(
        workspace_view.values(),
        headers=WorkspaceView.headers(),
        tablefmt="grid"))
