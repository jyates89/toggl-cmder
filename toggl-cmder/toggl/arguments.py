'''
Class with static methods that simply set up the
arguments we expect.
'''
class Arguments(object):
    @staticmethod
    def insert_main_arguments(argument_parser):
        argument_parser.add_argument(
            '--token',
            type=str,
            help='Specify the token string to use.')

        argument_parser.add_argument(
            '--token-reset',
            action='store_true',
            help="Reset the API token used for toggl.")

        argument_parser.add_argument(
            '--verbosity', '-v',
            action='count',
            help='Increase verbosity.',
            default=3)

        argument_parser.add_argument(
            '--only-cached',
            action='store_true',
            help="Only read from cached data.")

        argument_parser.add_argument(
            '--list-projects',
            action='store_true')

        argument_parser.add_argument(
            '--list-tags',
            action='store_true')

        argument_parser.add_argument(
            '--list-time-entries',
            action='store_true')

        argument_parser.add_argument(
            '--list-workspaces',
            action='store_true')

        argument_parser.add_argument(
            '--stop-timer',
            action='store_true',
            help='Stop the current timer.')

        argument_parser.add_argument(
            '--current',
            help="Get current timer.",
            action='store_true')

    @staticmethod
    def insert_start_timer_arguments(sub_argument_parser):
        start_timer_args = sub_argument_parser.add_parser(
            "start-timer",
            help="Start a new toggl timer.")

        start_timer_args.add_argument(
            '--tags',
            help='Tags for this timer.',
            nargs='?',
            default=[])

        start_timer_args.add_argument(
            '--description',
            help="Description of the timer.",
            required=True)

        start_timer_args.add_argument(
            '--project',
            help='Project for this timer.')

        start_timer_args.add_argument(
            '--workspace',
            help='Workspace for this timer.')

    @staticmethod
    def insert_add_timer_arguments(sub_argument_parser):
        add_timer_args = sub_argument_parser.add_parser(
            'add-timer',
            help='Create a new timer.')

        add_timer_args.add_argument(
            '--description',
            help="Description of the timer.",
            required=True)

        add_timer_args.add_argument(
            '--project',
            help="Project for this timer.")

        add_timer_args.add_argument(
            '--workspace',
            help="Workspace for this timer.")

        add_timer_args.add_argument(
            '--tags',
            help="Tags for this timer.",
            nargs='?',
            default=[])

        add_timer_args.add_argument(
            '--start',
            help="Start time for this timer.",
            required=True)

        add_timer_args.add_argument(
            '--stop',
            help="Stop time for this timer.",
            required=True)

    @staticmethod
    def insert_add_project_arguments(sub_argument_parser):
        add_project_args = sub_argument_parser.add_parser(
            'add-project',
            help='Create a new project.')

        add_project_args.add_argument(
            '--name',
            help='Name of the project to add.',
            required=True)

        add_project_args.add_argument(
            '--workspace',
            help='Workspace where this project belongs.',
            required=True)

    @staticmethod
    def insert_add_tag_arguments(sub_argument_parser):
        add_tag_args = sub_argument_parser.add_parser(
            'add-tag',
            help='Add a new tag.')

        add_tag_args.add_argument(
            '--name',
            help='Name of the new tag.',
            required=True)

        add_tag_args.add_argument(
            '--workspace',
            help='Workspace where this tag belongs.',
            required=True)
