# toggl-cmder

This script allows a user to control Toggl via the REST API.

## Installation

From the directory where you cloned this repository:
`python3 -m venv $(pwd)/venv`
`source $(pwd)/venv/bin/activate`
`pip install -r requirements.txt`

## Usage Requirements

You must log in to the Toggl site and retrieve the API key to access the API using this script.
1. Login to the Toggl site.
2. Go to https://toggl.com/app/profile and find the API key at the bottom of the page.
3. Create a file called `.api_token` and place the token inside the file.
4. You may test the connection by simply running `python toggle-cmder --list-workspaces`.

## Usage
```
usage: python toggl-cmder [-h] [--token TOKEN] [--token-reset] [--verbosity]
                          [--list-projects] [--list-tags]
                          [--list-time-entries] [--list-workspaces]
                          [--stop-timer] [--current]
                          {start-timer,add-project,add-timer,add-tag} ...

Control toggl via the REST API. (v1.0.0)

positional arguments:
  {start-timer,add-project,add-timer,add-tag}
    start-timer         Start a new toggl timer.
    add-project         Create a new project.
    add-timer           Create a new timer.
    add-tag             Add a new tag.

optional arguments:
  -h, --help            show this help message and exit
  --token TOKEN         Specify the token string to use.
  --token-reset         Reset the API token used for toggl.
  --verbosity, -v       Increase verbosity.
  --list-projects
  --list-tags
  --list-time-entries
  --list-workspaces
  --stop-timer          Stop the current timer.
  --current             Get current timer.
```

## Troubleshooting

If there are any issues you have come across, please open a new issue or email me.

## Limitations

You cannot, at this time, use this script to delete items.
