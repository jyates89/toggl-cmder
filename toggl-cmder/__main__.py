import requests
import json

from toggl.project import Project, ProjectEncoder, ProjectResponseDecoder
from toggl.workspace import Workspace, WorkspaceResponseDecoder

from requests.auth import HTTPBasicAuth

token = 'a5747ea126cf28cb363cd892c316bf9e'

toggl_auth = HTTPBasicAuth(token, 'api_token')

workspaces = requests.get('https://www.toggl.com/api/v8/workspaces',
                      auth=toggl_auth)

projects_url = "https://www.toggl.com/api/v8/workspaces/{}/projects"

for workspace in json.loads(workspaces.text, cls=WorkspaceResponseDecoder):
    projects = requests.get(projects_url.format(workspace.id),
                            auth=toggl_auth)
    for project in json.loads(projects.text, cls=ProjectResponseDecoder):
        print(project.name)

if __name__ == "__main__":
    pass
