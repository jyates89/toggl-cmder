
import argparse
import logging

from toggl import interface

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(
        description='Control toggl via the REST API.')

    arg_parser.add_argument('--token', type=str,
                            help='Specify the token string to use.')
    arg_parser.add_argument('--token-reset',
                            action='store_true',
                            help="Reset the API token used for toggl.")

    sub_arg_parsers = arg_parser.add_subparsers()

    start_timer_args = sub_arg_parsers.add_parser("start-timer",
                                                  help="Start a new toggl timer.")
    start_timer_args.add_argument('--description',
                                  help="Description of the timer.",
                                  required=True)
    start_timer_args.add_argument('--project',
                                  help='Project for this timer.')
    start_timer_args.add_argument('--tags',
                                  help='Tags for this timer.',
                                  nargs='?',
                                  default=[])
    start_timer_args.add_argument('--workspace',
                                  help='Workspace for this timer.')

    arg_parser.add_argument('--stop-timer',
                            action='store_true',
                            help='Stop the current timer.')

    add_project_args = sub_arg_parsers.add_parser('add-project',
                                                  help='Create a new project.')
    add_project_args.add_argument('--name',
                                  help='Name of the project to add.')
    add_project_args.add_argument('--workspace',
                                  help='Workspace where this project belongs.')

    add_tag_args = sub_arg_parsers.add_parser('add-tag',
                                              help='Add a new tag.')
    add_tag_args.add_argument('--name',
                              help='Name of the new tag.')
    add_tag_args.add_argument('--workspace',
                              help='Workspace where this tag belongs.')

    token = ""

    args = arg_parser.parse_args()

    logger = logging.getLogger()
    log_file_handle = logging.FileHandler('toggl-cmder.log')
    log_stream_handle = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s: %(levelname)s: %(module)s: %(lineno)d: %(message)s",
        "%Y-%m-%dT%H:%M:%S")
    log_file_handle.setFormatter(formatter)
    log_stream_handle.setFormatter(formatter)
    logger.addHandler(log_file_handle)
    logger.addHandler(log_stream_handle)
    if args.verbose:
        logger.setLevel(args.verbose)

    if args.token:
        token = args.token
    else:
        try:
            token_file = open('.api_token', 'r')
            token = token_file.read()
            token_file.close()
        except FileNotFoundError:
            print("please create the token file '.api_token")
            exit(1)

    instance = interface.Interface(api_token=token,
                                   logger=logger)
    if not instance.test_connection():
        raise RuntimeError("authentication failure")

    if args.token_reset:
        instance.reset_user_token()


    workspaces = []
    projects = []
    tags = []

    for workspace in instance.download_workspaces():
        for project in instance.download_projects(workspace):
            print(type(project.id))
            print(type(project.created))
        for tag in instance.download_tags(workspace):
            tags.append(tag)
    user_data = instance.download_userdata()


    if token == user_data.api_token:
        print("no token update needed")
    else:
        print("updating token file")
        file = open('.api_token', 'w')
        file.write(user_data.api_token)
        file.close()

    instance.create_time_entry(
        workspaces[0],
        projects[0],
        [tags[0]],
        "",
    )
