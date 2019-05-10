
from toggl import interface

token = 'a5747ea126cf28cb363cd892c316bf9e'

if __name__ == "__main__":
    instance = interface.Interface(api_token=token)

    workspaces = []
    projects = []
    tags = []
    for workspace in instance.download_workspaces():
        workspaces.append(workspace)
        for project in instance.download_projects(workspace):
            projects.append(project)
        for tag in instance.download_tags(workspace):
            tags.append(tag)

    instance.create_time_entry(
        workspaces[0],
        projects[0],
        [tags[0]],
        "",
    )
