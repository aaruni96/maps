#!/usr/bin/python3
"""This module provides package management functionality for MaRDI"""
import os
import sys
import subprocess
import tempfile
import argparse
import gi
gi.require_version("OSTree", "1.0")
from gi.repository import OSTree, GLib

VERSION = '0.1-alpha'
BWRAP = '/home/akaushik/Programs/git/Github/bubblewrap/bwrap'
OSTREE_REPO_MODE_BARE_USER = 2


# Define a CLI
def addCLI():
    """Function adds a CLI to the package."""
    parser = argparse.ArgumentParser(
        prog='maps',
        description=("maps - MaRDI Packaging System : "
                     "Provides a unified interface for packaging "
                     "and deploying software environments."
                     ),
    )
    parser.add_argument('--version', action='version', version=VERSION)
    parser.add_argument('-c', '--commit', dest='COMMIT', nargs=2, metavar=("TREE", "BRANCH"),
                        default=False, help="Commit TREE to BRANCH in REPO")
    parser.add_argument('-i', '--initialize', dest='DIR',
                        help="initialize DIR with a good base tree")
    parser.add_argument('-d', '--deploy', dest='DEPLOY', action='store',
                        default=False, help="deploy mode, for installing environments")
    parser.add_argument('-p', '--package', dest='PACKAGE', action='store_true',
                        default=False, help="package mode for defining "
                        "and publishing new environments")
    parser.add_argument('--repo', dest='REPO',
                        help="Repository to use")
    parser.add_argument('-r', '--run', dest='RUN', action='store',
                        default=False, help="Repository to use")
    parser.add_argument('-s', '--sandbox', dest='LOCATION',
                        help="Start a sandbox at LOCATION")
    parser.add_argument('-v', '--verbose', dest='VERBOSE', action='store_true',
                        help="enable verbose output")
    return parser


# if the directory does not exist, assume we're doing a first run, go through initialization
def program_init(repopath):
    """Function verifies requirements, and initializes the working directories"""
    # step 1 : check bwrap, and overlayfs-fuse are installed
    assert os.path.isfile(BWRAP)
    assert os.path.isfile("/usr/bin/fuse-overlayfs")
    # step 2 : create the directory, so the function is not called again
    subprocess.run(f"mkdir -pv {'/'.join(repopath.split('/'))}".split(), check=True)


def mode_run(args):
    """Function to execute a published environment"""
    # check if the path exists
    DATADIR = f"{os.getenv('HOME')}/.var/org.mardi.maps/{args.RUN}"
    if not os.path.isdir(DATADIR):
        raise AssertionError(f"Data directory does not exist. Is {args.RUN} installed ?")
    # setup live directory
    subprocess.run(["fuse-overlayfs", "-o", f"lowerdir={DATADIR}/rofs", "-o",
                    f"upperdir={DATADIR}/rwfs", "-o", f"workdir={DATADIR}/tmpfs",
                    f"{DATADIR}/live"], check=True)

    # launch sandbox
    print(f"Launching {args.RUN}...")
    rstatus = subprocess.run([BWRAP, "--no-int-term", "--unshare-user", "--unshare-pid",
                              "--bind", f"{DATADIR}/live", "/", "--proc", "/proc", "--dev", "/dev",
                              "--uid", "0", "--gid", "0", "bash"], check=False)
    if rstatus.returncode != 0:
        print(f"Sandbox exited with return code {rstatus.returncode}")
    # when the sandbox exits, cleanup
    # can this fail? how do we handle that scenario?
    subprocess.run(["fusermount", "-u", f"{DATADIR}/live"], check=False)


# Deploy Mode
def mode_deploy(repo, args):
    """Function to deploy from repo to local disk"""
    # Right now, we only checkout things from the local ostree repo
    # Later, we also need to check from a trusted remote, if not found in the local repo
    DATADIR = f"{os.getenv('HOME')}/.var/org.mardi.maps/{args.DEPLOY}"
    PDATADIR = '/'.join(DATADIR.split('/')[0:-1])
    subprocess.run(f"mkdir -pv {PDATADIR}".split(), check=True)
    ret = subprocess.run(f"mkdir -v {DATADIR}".split(), check=False)
    subprocess.run(f"mkdir -pv {DATADIR}/rwfs".split(), check=False)
    subprocess.run(f"mkdir -pv {DATADIR}/tmpfs".split(), check=False)
    subprocess.run(f"mkdir -pv {DATADIR}/live".split(), check=False)
    if ret.returncode != 0:
        raise AssertionError("Error: Could not create directory. "
                             "Path already exists, or other unknown error")
    refhash = repo.list_refs()[1][args.DEPLOY]
    tfd = os.open(DATADIR, os.O_RDONLY)
    repo.checkout_at(None, tfd, "rofs", refhash, None)
    print(f"Success... {args.DEPLOY} is now ready to use!")


# Package Mode
def mode_package(repo, args):
    """Function for package mode. Not intended to be used by "end users" """
    if args.DIR is not None:
        refhash = ''
        if 'base/x86_64/debian' not in list(repo.list_refs()[1].keys()):
            # import base to local repo
            refhash = repo.remote_list_refs("NameOfRemote")[1]['base/x86_64/debian']
            repo.pull("NameOfRemote", [refhash], OSTree.RepoPullFlags(4), None, None)
        else:
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
        repo.prepare_transaction()
        mutree = OSTree.MutableTree.new()
        mfd = os.open('/'.join(args.COMMIT[0].split('/')[0:-1]), os.O_RDONLY)
        repo.write_dfd_to_mtree(mfd, args.COMMIT[0].split('/')[-1], mutree, None, None)
        mfile = repo.write_mtree(mutree, None)
        mcommit = repo.write_commit(None, None, None, None, mfile[1], None)
        print(mcommit[1])
        repo.transaction_set_ref(None, args.COMMIT[1], mcommit[1])
        repo.commit_transaction(None)
        _, refs = repo.list_refs()
        print(list(refs.keys()))


def sanity_checks(parser, args):
    """Some simply sanity checks, before the program proceeds"""
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    if not args.PACKAGE and args.RUN is False:
        if args.DEPLOY is False:
            raise AssertionError("This is an impossible case, I think?")
        if args.DIR is not None:
            raise AssertionError("Can only initialize a dir in package mode!")
        if args.LOCATION is not None:
            raise AssertionError("As of now, sandboxing is only supported as a part of packaging.")
        if args.COMMIT is not False:
            raise AssertionError("Can only commit to repo in package mode!")
    else:
        if args.DEPLOY is not False:
            raise AssertionError("Cannot open in package mode and deploy mode simultaneously! "
                                 "Please check arguments!")


# Main function
def main():
    """Main function"""
    parser = addCLI()
    args = parser.parse_args()

    # Some sanity checks
    sanity_checks(parser, args)

    # Setup
    if os.getenv('XDG_DATA_HOME') is not None:
        data = os.getenv('XDG_DATA_HOME')
    else:
        # this will crash if HOME is not set. How likely?
        data = f"{os.getenv('HOME')}/.local/share"
    data = f"{data}/org.mardi.maps"
    if args.REPO is None:
        repopath = f"{data}/ostree/repo"
    else:
        repopath = args.REPO
    repo = repopath.split('/')[-1]
    repopath = '/'.join(repopath.split('/')[0:-1])

    if not os.path.isdir(repopath):
        program_init(repopath)

    fd = os.open(repopath, os.O_RDONLY)
    repo = OSTree.Repo.create_at(fd, repo,
                                 OSTree.RepoMode(OSTREE_REPO_MODE_BARE_USER), None, None)
    repo.open(None)
    # Configure a good known remote, if not already present
    if (not repo.remote_list()) or "NameOfRemote" not in repo.remote_list():
        repo.remote_add("NameOfRemote", "http://maunzerle:81",
                        GLib.Variant('a{sv}', {"gpg-verify": GLib.Variant('b', False)}), None)

    # Run mode
    if args.RUN is not False:
        mode_run(args)
    # Deploy mode
    elif args.DEPLOY is not False:
        mode_deploy(repo, args)
    # Package mode
    else:
        mode_package(repo, args)


if __name__ == "__main__":
    main()
