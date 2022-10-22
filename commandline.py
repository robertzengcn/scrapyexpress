# -*- coding: utf-8 -*-

import argparse
from version import __version__


def get_command_line(only_print_help=False):
    """
    Parse command line arguments when emailscrapy is used as a CLI application.

    Returns:
        The configuration as a dictionary that determines the behaviour of the app.
    """

    parser = argparse.ArgumentParser(prog='scrapyexpress',
                                     description='grab email from aliexpress site',
                                     epilog='Emailscrapy {version}. '
                                            'Please use it on your own risk. (c) by Robert Zeng'
                                            ', 2012-2019.')

    parser.add_argument('-k', '--keyword', type=str, action='store',default='',
                        help='keyword pass to the program '
                        )


    parser.add_argument('-f', '--keyfile', type=str, action='store', default='',
                        help='the file the contain keyword')

                        

    if only_print_help:
        parser.print_help()
    else:
        args = parser.parse_args()

        return vars(args)
