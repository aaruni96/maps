#!/usr/bin/python3

"""This module does blahblahblah"""

import argparse

VERSION = '0.1-alpha'

# Define a CLI
parser = argparse.ArgumentParser(
    prog='maps',
    description=(
        "maps - MaRDI Packaging System :"
        "Provides a unified interface for packaging and deploying software environments."
        ),
    epilog="In case of conflicting arguments, the one at the last wins."
    )

parser.add_argument('--version', action='version', version=VERSION)

parser.add_argument('-i', '--initialize', dest="DIR",
                    help="initialize DIR with a good base tree")
parser.add_argument('-d', '--deploy', dest='DEPLOY', action='store_true',
                    default=True, help="deploy mode, for installing environments (default)")
parser.add_argument('-p', '--package', dest='PACKAGE', action='store_false',
                    help="package mode, for defining and publishing new environments")
parser.add_argument('-v', '--verbose', dest='VERBOSE', action='store_true',
                    help="enable verbose output")

args = parser.parse_args()

print(args)
