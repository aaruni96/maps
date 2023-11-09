# MaPS - MaRDI Packaging System

## Introduction

MaPS, short for MaRDI Packaging System is the working name for the software system created by TA1 **Computer Algebra** for Measure 1.4 **Predefined software environments**. MaPS provides a unified interface both, to package a software inside a functional environment (called a _runtime_), and to "install" a published runtime onto a computer system in a user friendly way, while still keeping it separate from the computer's host environment.

## WiKi

Have a look at the wiki, located at https://github.com/aaruni96/maps/wiki

### Bubblewrap

We currently depend on a patched version of bubblewrap to avoid minor problem in how SIGINT is handled. Until the fix (or equivalent) is bundled into release, we need to clone and compile `https://github.com/aaruni96/bubblewrap/tree/ak/sigint` . `maps` will automatically try to do this for you, but you must ensure you have the devtools installed to compile bwrap.

## Installing

We have ambitions of packaing `maps` in `apt`/`dnf`/`aur`/whatever. In the meantime, it must be cloned from git, and run as a python script, ideally within a venv.

```bash
git clone git@github.com:aaruni96/maps.git
cd maps
python3 -m venv .venv
source .venv/bin/activate
pip install pygobject tomli
```

Then, use maps using the venv'ed python interpretor. So, replace each invocation of `maps` in the documentation with `python src/maps.py` .

## Usage

### Installing Runtimes

Installing and running a runtime is a simple case of providing the unique identifier of the runtime to `maps`.

```bash
maps --deploy me.myname.myapplication/sysarch/version
maps --run me.myname.myapplication/sysarch/version
```

### Packaging Runtimes

In this mode, the user can commit arbitrary trees into an ostree repo, and then (sometime in the future) publish them. The trees contain everything required by the application to run, as the resulting package will be run inside a user namespace sandbox. The packager is responsible for providing a correct tree, although, we provide a "default" tree (based on the debian docker image) to begin with.

```bash
# Initialise a new tree from a minimal debian base
maps --package --initialize /path/to/new/tree

# Start a bash session inside a sandbox
maps --package --sandbox /path/to/new/tree

# Commit the tree into ostree repository
maps --package --commit /path/to/new/tree me.myname.myapplication/sysarch/version
```

## Known Problems

 - The OSTree Repository cannot be initialized onto a filesystem without extended attributes, in particular, NFS does not work. As a workaround, you can set the environment variables `XDG_DATA_HOME` (system OSTree Repository) and `HOME` (Runtime checkout) to point to some directory on a filesystem which has support for extended attributes.
  - There is currently a bug in [fuse-overlayfs](https://github.com/containers/fuse-overlayfs/issues/399), which causes problems in copying a read-only file. In concrete terms, this means that `julia` testing infrastructure fails at the time of writing. This needs to be either patched in upstream, or worked around by `maps`.
  - Only Linux is supported directly. MacOS and Windows users are recommended to virtualize Linux in their respective environments. More information about this is in the [Wiki](https://github.com/aaruni96/maps/wiki/Non-Linux-OSs).


## Contributing

### Style Practices

All code must conform to these settings of pylint and flake8

```bash
pylint -d C0413,C0103,R0912,R0915,W0603 src/maps.py
flake8 --max-line-length 100 --ignore=E402 src/maps.py
```

