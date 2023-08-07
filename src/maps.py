#!/usr/bin/python3

"""This module does blahblahblah"""

import os
import gi
import tempfile
import argparse

gi.require_version("OSTree", "1.0")

from gi.repository import OSTree, Gio

VERSION = '0.1-alpha'

# Define a CLI
parser = argparse.ArgumentParser(
    prog='maps',
    description=(
        "maps - MaRDI Packaging System :"
        "Provides a unified interface for packaging and deploying software environments."
        ),
    epilog="In case of conflicting arguments, the one which comes later wins."
    )
parser.add_argument('--version', action='version', version=VERSION)
parser.add_argument('-i', '--initialize', dest="DIR",
                    help="initialize DIR with a good base tree")
parser.add_argument('-d', '--deploy', dest='DEPLOY', action='store_true',
                    default=False, help="deploy mode, for installing environments (default)")
parser.add_argument('-p', '--package', dest='PACKAGE', action='store_true',
                    default=False, help="package mode, for defining and publishing new environments")
parser.add_argument('-v', '--verbose', dest='VERBOSE', action='store_true',
                    help="enable verbose output")
args = parser.parse_args()

print(args)

if (args.PACKAGE):
    if (args.DEPLOY):
        raise Exception("Cannot open in package mode and deploy mode simultaneously! Please check arguments!")
    if ( args.DIR != None ):
        # step 1 : checkout repo to tmp
        # step 2 : copy (reflink=auto) tmp to DIR
        # step 3 : delete tmp
        repopath = 'repo'
        # later, $XDG_DATA_HOME/maps/repo
        fd = os.open('ostree', os.O_RDONLY)
        repo = OSTree.Repo.open_at(fd, repopath, None)
        #repo = 
        repo.open(None)
        refhash=repo.list_refs()[1]['base/x86_64/debian']
        with tempfile.TemporaryDirectory() as tmpdir:
            tfd = os.open(tmpdir, os.O_RDONLY)
            repo.checkout_at(None, tfd, "ostree", refhash, None)
            if (os.system(f"mkdir -v {args.DIR}") == 0):
                os.system(f"cp -r --reflink=auto {tmpdir}/ostree/* {args.DIR}/")
            else:
                print(f"ERROR: Could not create {args.DIR}! Bailing!")