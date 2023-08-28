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
BWRAP_DEFAULT = f"{'/'.join(__file__.split('/')[0:-2])}/deps/bubblewrap/bwrap"
if os.getenv('BWRAP_CMD') is not None:
    BWRAP = str(os.getenv('BWRAP_CMD'))
else:
    BWRAP = BWRAP_DEFAULT
OVERLAYFS = '/usr/bin/fuse-overlayfs'
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
    parser.add_argument('--add-remote', dest='REMOTE', nargs=2,
                        metavar=("REMOTE_NAME", "REMOTE_URL"), action='store',
                        default=False, help="Add REMOTE to local ostree repo")
    parser.add_argument('-c', '--commit', dest='COMMIT', nargs=2, metavar=("TREE", "BRANCH"),
                        default=False, help="Commit TREE to BRANCH in REPO")
    parser.add_argument('-d', '--deploy', dest='DEPLOY', action='store',
                        default=False, help="deploy mode, for installing environments")
    parser.add_argument('--del-remote', dest="DEL_REMOTE", action='store',
                        default=False, help="Delete REMOTE from local ostree repo")
    parser.add_argument('-i', '--initialize', dest='DIR',
                        help="initialize DIR with a good base tree")
    parser.add_argument('-l', '--list', dest='LIST', action='store_true',
                        default=False, help="List available environments")
    parser.add_argument('-p', '--package', dest='PACKAGE', action='store_true',
                        default=False, help="package mode for defining "
                        "and publishing new environments")
    parser.add_argument('--repo', dest='REPO',
                        help="Repository to use")
    parser.add_argument('--reset', dest='RESET', action='store_true',
                        default=False, help="Reset the runtime")
    parser.add_argument('-r', '--run', dest='RUN', action='store',
                        default=False, help="Repository to use")
    parser.add_argument('-s', '--sandbox', dest='LOCATION',
                        help="Start a sandbox at LOCATION")
    parser.add_argument('-v', '--verbose', dest='VERBOSE', action='store_true',
                        help="enable verbose output")
    return parser


def sanity_checks(parser, args):
    """Some simply sanity checks, before the program proceeds"""
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    if not args.PACKAGE and args.RUN is False and args.LIST is False:
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


def program_init(repopath):
    """Init function verifies requirements, sets up the repo. Returns the OSTree Repo."""
    # step 1 : check bwrap, and overlayfs-fuse are installed
    if (BWRAP == BWRAP_DEFAULT) and not os.path.isfile(BWRAP):
        # clone and compile bubblewrap
        subprocess.run(["git", "clone", "git@github.com:aaruni96/bubblewrap.git", BWRAP[0:-5]],
                       check=False)
        subprocess.run(f"cd {BWRAP[0:-5]} && git checkout ak/sigint", shell=True, check=False)
        subprocess.run(f"cd {BWRAP[0:-5]} && ./autogen.sh && ./configure && make -j", shell=True,
                       check=True)
    assert os.path.isfile(BWRAP)
    assert os.path.isfile(OVERLAYFS)
    # step 2 : create the directory
    subprocess.run(f"mkdir -pv {'/'.join(repopath.split('/'))}".split(), check=True)

    # step 3 : Configure a good known remote, if not already present
    repo = repopath.split('/')[-1]
    repopath = '/'.join(repopath.split('/')[0:-1])
    fd = os.open(repopath, os.O_RDONLY)
    repo = OSTree.Repo.create_at(fd, repo,
                                 OSTree.RepoMode(OSTREE_REPO_MODE_BARE_USER),
                                 GLib.Variant('a{sv}', {}), None)
    if (not repo.remote_list()) or "Official" not in repo.remote_list():
        repo.remote_add("Official", "http://maunzerle:81",
                        GLib.Variant('a{sv}', {"gpg-verify": GLib.Variant('b', False)}), None)
        print("Automatically adding official remote")
    return repo


def make_remote_ref_list(repo, remote):
    """Given a repo and a remote, return a list of refs in the remote of that repo"""
    if remote is None:
        return []
    if repo.remote_list() is None:
        print(f"Repo {repo} has no remotes!")
        return []
    if repo.remote_list() is not None:
        if remote not in repo.remote_list():
            print(f"Repo {repo} has no remote {remote}!")
            return []
    remote_refs = []
    remote_refs.extend(list(repo.remote_list_refs(remote)[1].keys()))
    return remote_refs


def mode_list(repo):
    """Prints a list of available refs"""
    print("Available runtimes are :")
    refs = list(repo.list_refs()[1].keys())
    if refs:
        print("Local")
        for ref in sorted(refs):
            print(f"\t - {ref}")
    remotes = repo.remote_list()
    for remote in remotes:
        remote_refs = make_remote_ref_list(repo, remote)
        if remote_refs:
            print(remote)
            for ref in sorted(remote_refs):
                print(f"\t - {ref}")

def mode_remotes(repo, args):
    """Administrative mode for remotes of the repo"""
    if args.REMOTE is not False:
        repo.remote_add(args.REMOTE[0], args.REMOTE[1],
                        GLib.Variant('a{sv}', {"gpg-verify": GLib.Variant('b', False)}), None)
        print(f"Added {args.REMOTE} to list of remotes!")
        return
    if args.DEL_REMOTE is not False:
        repo.remote_delete(args.DEL_REMOTE)
        print(f"Deleted {args.DEL_REMOTE} from list of remotes!")
        return
    pass


def mode_run(args):
    """Function to execute a published environment"""
    # check if the path exists
    DATADIR = f"{os.getenv('HOME')}/.var/org.mardi.maps/{args.RUN}"
    if not os.path.isdir(DATADIR):
        raise AssertionError(f"Data directory does not exist. Is {args.RUN} installed ?")
    # check if reset is requested
    if args.RESET:
        subprocess.run(f"rm -rf {DATADIR}/live/*".split(), check=True)
        return
    # setup live directory
    subprocess.run(["fuse-overlayfs", "-o", f"lowerdir={DATADIR}/rofs", "-o",
                    f"upperdir={DATADIR}/rwfs", "-o", f"workdir={DATADIR}/tmpfs",
                    f"{DATADIR}/live"], check=True)

    # launch sandbox
    print(f"Launching {args.RUN}...")
    senv = os.environ
    senv["HOME"] = "/home/runtime"
    senv["PS1"] = "\\u@runtime:\\w# "
    rstatus = subprocess.run([BWRAP, "--no-int-term", "--unshare-user", "--unshare-pid",
                              "--bind", f"{DATADIR}/live", "/", "--proc", "/proc", "--dev", "/dev",
                              "--uid", "0", "--gid", "0", "bash"], env=senv, check=False)
    if rstatus.returncode != 0:
        print(f"Sandbox exited with return code {rstatus.returncode}")
    # when the sandbox exits, cleanup
    # can this fail? how do we handle that scenario?
    subprocess.run(["fusermount", "-u", f"{DATADIR}/live"], check=False)


# Deploy Mode
def mode_deploy(repo, args):
    """Function to deploy from repo to local disk"""
    refhash = ''
    if args.DEPLOY in repo.list_refs()[1]:
        refhash = repo.list_refs()[1][args.DEPLOY]
    elif args.DEPLOY in [j for remotes in repo.remote_list()
                         for j in make_remote_ref_list(repo, remotes)]:
        for remote in repo.remote_list():
            if args.DEPLOY in repo.remote_list_refs(remote)[1]:
                refhash = repo.remote_list_refs(remote)[1][args.DEPLOY]
                repo.pull(remote, [refhash], OSTree.RepoPullFlags(4), None, None)
                break
    else:
        print("Error: environment not found! Use list mode --list to view available runtimes.")
        sys.exit(1)
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
    tfd = os.open(DATADIR, os.O_RDONLY)
    osopts = blank_options()
    osopts.bareuseronly_dirs = True
    osopts.mode = OSTree.RepoCheckoutMode(1)
    repo.checkout_at(osopts, tfd, "rofs", refhash, None)
    print(f"Success... {args.DEPLOY} is now ready to use!")


def blank_options():
    """Return an OSTree.RepoCheckoutAtOptions object,
    with all (most) options blanked out explicitly """
    opts = OSTree.RepoCheckoutAtOptions()
    opts.bareuseronly_dirs = False
    # opts.devino_to_csum_cache =
    opts.enable_fsync = False
    opts.enable_uncompressed_cache = False
    # opts.filter =
    # opts.filter_user_data =
    opts.force_copy = False
    opts.force_copy_zerosized = False
    opts.mode = OSTree.RepoCheckoutMode(0)
    opts.no_copy_fallback = False
    opts.overwrite_mode = OSTree.RepoCheckoutOverwriteMode(0)
    opts.process_passthrough_whiteouts = False
    opts.process_whiteouts = False
    # opts.sepolicy
    opts.sepolicy_prefix = ''
    # opts.subpath = ''
    # opts.unused_bools = []
    # opts.unused_ints = []
    # opts.unused_ptrs = []
    return opts


# Package Mode
def mode_package(repo, args):
    """Function for package mode. Not intended to be used by "end users" """
    if args.DIR is not None:
        refhash = ''
        if 'base/x86_64/debian' not in list(repo.list_refs()[1].keys()):
            # import base to local repo
            refhash = repo.remote_list_refs("Official")[1]['base/x86_64/debian']
            repo.pull("Official", [refhash], OSTree.RepoPullFlags(4), None, None)
        else:
            refhash = repo.list_refs()[1]['base/x86_64/debian']
        with tempfile.TemporaryDirectory() as tmpdir:
            tfd = os.open(tmpdir, os.O_RDONLY)
            osopts = blank_options()
            osopts.bareuseronly_dirs = True
            osopts.mode = OSTree.RepoCheckoutMode(1)
            repo.checkout_at(osopts, tfd, "ostree", refhash, None)
            if os.system(f"mkdir -v {args.DIR}") == 0:
                os.system(f"cp -r --reflink=auto {tmpdir}/ostree/* {args.DIR}/")
                print(f"Successfully initialized a base debian tree at {args.DIR} !")
            else:
                print(f"ERROR: Could not create {args.DIR}! Bailing!")
    if args.LOCATION is not None:
        # location is a functional tree, we just have to sandbox in it
        # its the user's responsibility to ensure the tree is good
        print(f"Launching a sandbox in {args.LOCATION}...")
        senv = os.environ
        senv["HOME"] = "/home/runtime"
        senv["PS1"] = "\\u@runtime:\\w# "
        rstatus = subprocess.run([BWRAP, "--no-int-term", "--unshare-user", "--unshare-pid",
                                  "--bind", args.LOCATION, "/", "--proc", "/proc", "--dev", "/dev",
                                  "--uid", "0", "--gid", "0", "bash", "--norc"],
                                 env=senv, check=False)
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

    repo = program_init(repopath)

    # Run mode
    if (args.REMOTE is not False) or (args.DEL_REMOTE is not False):
        mode_remotes(repo, args)
    elif args.LIST is not False:
        mode_list(repo)
    elif args.RUN is not False:
        mode_run(args)
    # Deploy mode
    elif args.DEPLOY is not False:
        mode_deploy(repo, args)
    # Package mode
    else:
        mode_package(repo, args)


if __name__ == "__main__":
    main()
