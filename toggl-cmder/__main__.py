
from toggl import interface

token = 'a5747ea126cf28cb363cd892c316bf9e'

if __name__ == "__main__":
    instance = interface.Interface(api_token=token)
    for workspace in instance.download_workspaces():
        for project in instance.download_projects(workspace):
            print(type(project.id))
            print(type(project.created))
        for tag in instance.download_tags(workspace):
            print(type(tag.id))
