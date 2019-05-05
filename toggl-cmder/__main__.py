
from toggl import interface

token = 'a5747ea126cf28cb363cd892c316bf9e'
projects_url = "https://www.toggl.com/api/v8/workspaces/{}/projects"

if __name__ == "__main__":
    instance = interface.Interface(api_token=token)
    for workspace in instance.download_workspaces():
        print(workspace.id)
