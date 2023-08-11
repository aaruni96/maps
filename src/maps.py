#!/usr/bin/python3
"""This module provides package management functionality for MaRDI"""
import os
import sys
import subprocess
import tempfile
import argparse
import gi
gi.require_version("OSTree", "1.0")
from gi.repository import OSTree

VERSION = '0.1-alpha'
BWRAP = '/home/akaushik/Programs/git/Github/bubblewrap/bwrap'
OSTREE_REPO_MODE_BARE_USER = 2

# Define a CLI
parser = argparse.ArgumentParser(
    prog='maps',
    description=("maps - MaRDI Packaging System : "
                 "Provides a unified interface for packaging and deploying software environments."
                 ),
)
parser.add_argument('--version', action='version', version=VERSION)
parser.add_argument('-c', '--commit', dest='COMMIT', nargs=2, metavar=("TREE", "BRANCH"),
                    default=False, help="Commit TREE to BRANCH in REPO")
parser.add_argument('-i', '--initialize', dest='DIR',
                    help="initialize DIR with a good base tree")
parser.add_argument('-d', '--deploy', dest='DEPLOY', action='store_true',
                    default=False, help="deploy mode, for installing environments (default)")
parser.add_argument('-p', '--package', dest='PACKAGE', action='store_true',
                    default=False, help="package mode for defining and publishing new environments")
parser.add_argument('-r', '--repo', dest='REPO',
                    help="Repository to use")
parser.add_argument('-s', '--sandbox', dest='LOCATION',
                    help="Start a sandbox at LOCATION")
parser.add_argument('-v', '--verbose', dest='VERBOSE', action='store_true',
                    help="enable verbose output")
args = parser.parse_args()

# Some sanity checks and defaults
if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)
if args.REPO is None:
    if os.getenv('XDG_DATA_HOME') is not None:
        DATA = os.getenv('XDG_DATA_HOME')
    else:
        # this will crash if HOME is not set. How likely?
        DATA = f"{os.getenv('HOME')}/.local/share"
    repopath = f"{DATA}/org.mardi.maps/ostree/repo"
else:
    repopath = args.REPO
repo = repopath.split('/')[-1]
repopath = '/'.join(repopath.split('/')[0:-1])
# make sure the directories right under repo are present
subprocess.run(["mkdir", "-p", "-v", f"{'/'.join(repopath.split('/')[0:-1])}"], check=True)

if not args.PACKAGE:
    args.DEPLOY = True
    if args.DIR is not None:
        raise AssertionError("Can only initialize a dir in package mode!")
    if args.LOCATION is not None:
        raise AssertionError("As of now, sandboxing is only supported as a part of packaging.")
    if args.COMMIT is not None:
        raise AssertionError("Can only commit to repo in package mode!")

if args.PACKAGE:
    if args.DEPLOY:
        raise AssertionError("Cannot open in package mode and deploy mode simultaneously!"
                             "Please check arguments!")
    if args.DIR is not None:
        # step 1 : checkout repo to tmp
        # step 2 : copy (reflink=auto) tmp to DIR
        # step 3 : delete tmp
        fd = os.open(repopath, os.O_RDONLY)
        repo = OSTree.Repo.create_at(fd, repo,
                                     OSTree.RepoMode(OSTREE_REPO_MODE_BARE_USER), None, None)
        repo.open(None)
        refhash = repo.list_refs()[1]['base/x86_64/debian']
        with tempfile.TemporaryDirectory() as tmpdir:
            tfd = os.open(tmpdir, os.O_RDONLY)
            repo.checkout_at(None, tfd, "ostree", refhash, None)
            if os.system(f"mkdir -v {args.DIR}") == 0:
                os.system(f"cp -r --reflink=auto {tmpdir}/ostree/* {args.DIR}/")
                print(f"Successfully initialized a base debian tree at {args.DIR} !")
            else:
                print(f"ERROR: Could not create {args.DIR}! Bailing!")
    if args.LOCATION is not None:
        # location is a functional tree, we just have to sandbox in it
        # its the user's responsibility to ensure the tree is good
        print(f"Launching a sandbox in {args.LOCATION}...")
        rstatus = subprocess.run([BWRAP, "--no-int-term", "--unshare-user", "--unshare-pid",
                                  "--bind", args.LOCATION, "/", "--proc", "/proc", "--dev", "/dev",
                                  "--uid", "0", "--gid", "0", "bash"], check=False)
        if rstatus.returncode != 0:
            print(f"Sandbox exited with return code {rstatus.returncode}")
    if args.COMMIT is not False:
        # we are given TREE and BRANCH. All we have to do is commit TREE to BRANCH
        # what happens if we are updating a branch? Is that even possible?
        fd = os.open(repopath, os.O_RDONLY)
        repo = OSTree.Repo.create_at(fd, repo,
                                     OSTree.RepoMode(OSTREE_REPO_MODE_BARE_USER), None, None)
        repo.open(None)
        repo.prepare_transaction()
        mutree = OSTree.MutableTree.new()
        mfd = os.open('/'.join(args.COMMIT[0].split('/')[0:-1]), os.O_RDONLY)
        repo.write_dfd_to_mtree(mfd, args.COMMIT[0].split('/')[-1], mutree, None, None)
        mfile = repo.write_mtree(mutree, None)
        mcommit = repo.write_commit(None, None, None, None, mfile[1], None)
        print(mcommit[1])
        repo.transaction_set_ref(None, args.COMMIT[1], mcommit[1])
        repo.commit_transaction(None)
        status, refs = repo.list_refs()
        print(list(refs.keys()))
