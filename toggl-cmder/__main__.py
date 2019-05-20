
import argparse
import logging
import sys

from toggl import interface

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(
        description='Control toggl via the REST API.')

    arg_parser.add_argument('--token', type=str,
                            help='Specify the token string to use.')
    arg_parser.add_argument('--token-reset',
                            action='store_true',
                            help="Reset the API token used for toggl.")
    arg_parser.add_argument('--verbosity', '-v', action='count',
                            help='Increase verbosity.', default=0)

    sub_arg_parsers = arg_parser.add_subparsers(dest='parser_name')

    start_timer_args = sub_arg_parsers.add_parser("start-timer",
                                                  help="Start a new toggl timer.")
    start_timer_args.add_argument('--description',
                                  help="Description of the timer.")
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
                                  help='Name of the project to add.',
                                  required=True)
    add_project_args.add_argument('--workspace',
                                  help='Workspace where this project belongs.',
                                  required=True)

    add_tag_args = sub_arg_parsers.add_parser('add-tag',
                                              help='Add a new tag.')
    add_tag_args.add_argument('--name',
                              help='Name of the new tag.',
                              required=True)
    add_tag_args.add_argument('--workspace',
                              help='Workspace where this tag belongs.',
                              required=True)

    args = arg_parser.parse_args()
    if len(sys.argv) == 1:
        arg_parser.print_help()
        exit(0)

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

    # formula to convert 0-5 to actual inverted logging levels:
    # User enters 0 -> CRITICAL: 50
    # User enters 1 -> ERROR: 40
    # User enters 2 -> WARN: 30
    # User enters 3 -> INFO: 20
    # User enters 4 -> DEBUG: 10
    logger.setLevel((args.verbosity * -10) + 50)

    token = ""

    if args.token:
        token = args.token
    else:
        try:
            token_file = open('.api_token', 'r')
            token = token_file.read()
            token_file.close()
        except FileNotFoundError:
            logger.info("please create the token file '.api_token")
            exit(1)

    instance = interface.Interface(api_token=token,
                                   logger=logger)
    if not instance.test_connection():
        raise RuntimeError("authentication failure")

    user_data = instance.download_user_data()

    if args.token_reset:
        token = instance.reset_user_token()
        instance = interface.Interface(api_token=token,
                                       logger=logger)

    if token == user_data.api_token:
        logger.info("no token update needed")
    else:
        logger.info("updating token file")
        file = open('.api_token', 'w')
        file.write(user_data.api_token)
        file.close()

    if args.parser_name == 'start-timer':
        print('start-timer called')
    elif args.parser_name == 'add-tag':
        print('add-tag called')
    elif args.parser_name == 'add-project':

        print('add-project called')