# togglcmder

This script allows a user to control Toggl via the REST API.

## Features
* Complete control over Toggl projects, tags, and timers.
* Easily stop and resume timers.
    * `togglcmder timers stop`: will stop the current timer.
    * `togglcmder timers resume`: will resume the most recently stopped timer.
* Ability to download and view details on workspaces, projects, timers, and tags.
* Support for Python regex in all search fields, so that you don't need to know the
  exact name of an item to find it or restart it (or even delete it).
  * `togglcmder timers --workspace '.*' list`: list all timers in all workspaces.
  * `togglcmder timers list --description '^Python\s.*$'`: match any timer with
    Python in the description.
* Update projects, tags, and timers with various details.
    * Add a new tag to an old timer.
    * Remove tags from old timers.
    * Change the color designation of a project.

## Installation

From the directory where you cloned this repository:

`python3 -m venv $(pwd)/venv`

`source $(pwd)/venv/bin/activate`

`pip install -r requirements.txt`

From PyPI via pip:

`pip install togglcmder`

## Usage Requirements

You must log in to the Toggl site and retrieve the API key to access the API
using this script.

1. Login to the Toggl site.
2. Go to https://toggl.com/app/profile and find the API key at the bottom of the page.
3. Run the following command to initialize the configuration:
   1. `togglcmder --api-key b81d43def5cd60acea1e44ad319a7979`
4. You may test the connection by simply running `togglcmder workspaces`.
   1. It should at least list the 'Everything' workspace.

## Usage

The script will attempt to download data from the Toggl servers and store the
data in a local cache file. For Linux users this will be in ~/.config/togglcmder/cache.db.
This file is a SQLITE database. For Windows users it will be in %APPDATA%/togglcmder.
This tool has not been tested on Windows. You may pass `--help` to most sub commands to get more
information on them.

### Main Options

```
Usage: togglcmder [OPTIONS] COMMAND [ARGS]...

Options:
  --api-key TEXT                  Your API key for the Toggl API
  --reset-api-key                 Resets the Toggl API key and downloads it to
                                  the local device.
  --default-workspace TEXT        Specify a default workspace to use when
                                  otherwise not specified.
  --default-project TEXT          Specify a default project to use when
                                  otherwise not specified.
  --default-tags TEXT             Specify some default tags to always include
                                  for timers started on this machine.
  --default-time-entry-start-days INTEGER
                                  Specify some default start time to refresh
                                  time entries.
  --default-time-entry-stop-days INTEGER
                                  Specify some default stop time to refresh
                                  time entries.
  -v, --verbosity
  --version
  --sync                          Download from remote Toggl servers before
                                  attempting item lookups.  [default: False]
  --show-config                   Simply prints the current configuration.
  --help                          Show this message and exit.

Commands:
  projects    Add, update, delete, and list projects.
  tags        Add, update, delete, and list tags.
  timers      Add, update, delete, start, stop, and list timers.
  workspaces  List the currently available workspaces.

```

### Project Options

```
Usage: togglcmder projects [OPTIONS] COMMAND [ARGS]...

  Add, update, delete, and list projects.

Options:
  --workspace TEXT
  --help            Show this message and exit.

Commands:
  add
  delete
  list
  update

```

### Tag Options

```
Usage: togglcmder tags [OPTIONS] COMMAND [ARGS]...

  Add, update, delete, and list tags.

Options:
  --workspace TEXT
  --help            Show this message and exit.

Commands:
  add
  delete
  list
  update

```

### Timer Options

```
Usage: togglcmder timers [OPTIONS] COMMAND [ARGS]...

  Add, update, delete, start, stop, and list timers.

Options:
  --workspace TEXT
  --project TEXT
  --download-start VALIDATED_TIME
                                  This can be now[-/+[dhms]] or an iso
                                  formatted time string.
  --download-stop VALIDATED_TIME  This can be now[-/+[dhms]] or an iso
                                  formatted time string.
  --help                          Show this message and exit.

Commands:
  add      Add a completed time entry.
  current  Get the current running timer, if one exists.
  delete
  list
  resume   Resume the most recent timer.
  start    Start a new running timer.
  stop     Stop the current running timer, if one exists.
  update   Update an existing time entry with new details.

```

######NOTE

You can get more information on sub-commands by running help, for instance:
`togglcmder timers update --help`

#### Usage Examples

##### First Run

Required for usage.

`togglcmder --api-key b81d43def5cd60acea1e44ad319a7979`

##### Automatically Reset the API Key

This will automatically download and store a new API key for you.

`togglcmder --reset-api-key`

##### Setting Up a Default Workspace

`togglcmder --default-workspace Personal`

##### Setting Up a Default Project

`togglcmder --default-project CoolProject`

##### Listing All Projects in the Default Workspace

`togglcmder projects list`

##### Listing All Projects in a Specific Workspace

`togglcmder projects --workspace 'Work' list`

##### Adding a New Project to the Default Workspace

`togglcmder projects add --name 'Cool Project'`

##### Adding a New Tag to the Default Workspace

`togglcmder tags add --name 'cool_new_tag'`

##### Starting a New Timer with the Default Workspace and Project

`togglcmder timers start --description "I'm doing some work.." --tags "cool_new_tag,cool_old_tag"`

##### Display the Current Timer

`togglcmder timers current`

##### Stopping the Current Timer

`togglcmder timers stop`

##### Adding a Timer that has already Completed with Default Project and Workspace

`togglcmder timers add --description 'I already did this work.' --start-time "2020-03-10 01:00:00" --stop-time "2020-03-10 02:00:00" --tags "tag_one,tag_two"`

## Troubleshooting

If there are any issues you have come across, please open a new issue or email me.

## Limitations

* This does not support Toggl Pro; I have no plans to implement this support. Feel free to
  open a pull request if you feel like adding that kind of support!
