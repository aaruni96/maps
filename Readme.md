# MaPS - MaRDI Packaging System

![](https://img.shields.io/badge/version-0.4-blue)

## Introduction

MaPS, short for MaRDI Packaging System is the working name for the software system created by TA1
**Computer Algebra** for Measure 1.4 **Predefined software environments**. MaPS provides a unified
interface both, to package a software inside a functional environment (called a _runtime_), and to
"install" a published runtime onto a computer system in a user friendly way, while still keeping it
separate from the computer's host environment.

## WiKi

Have a look at the wiki, located at https://github.com/MaRDI4NFDI/maps/wiki

### Bubblewrap

We currently depend on a patched version of bubblewrap to avoid minor problem in how SIGINT is
handled. Until the fix (or equivalent) is bundled into release, we need to clone and compile
`https://github.com/aaruni96/bubblewrap/tree/ak/sigint` . `maps` will automatically try to do this
for you, but you must ensure you have the devtools installed to compile bwrap.

## Installing

We have ambitions of packaing `maps` in `apt`/`dnf`/`aur`/whatever. In the meantime, it must be
cloned from git, and run as a python script, ideally within a venv. Check the [installation
instructions on the wiki](https://github.com/MaRDI4NFDI/maps/wiki/Installation).

## Usage

### Installing Runtimes

Installing and running a runtime is a simple case of providing the unique identifier of the runtime
to `maps`.

```bash
# specifying the keyword `runtime` is optional
# if no other keyword is specified, it is assumed that one wishes to
# use the runtime mode (as it is the most common use of MaPS)
maps runtime --deploy me.myname.myapplication/sysarch/version
maps --run me.myname.myapplication/sysarch/version
```

### Packaging Runtimes

In this mode, the user can commit arbitrary filesystem trees into an ostree repo, and then (sometime
in the future) publish them. The tree contains everything required by the application to run, as the
resulting package will be run inside a user namespace sandbox. The packager is responsible for
providing a correct tree, although, we provide a "default" tree (based on the debian docker image)
to begin with.

```bash
# Initialise a new tree from a minimal debian base
maps package --initialize /path/to/new/tree

# Start a bash session inside a sandbox
maps package --sandbox /path/to/new/tree

# Commit the tree into ostree repository
maps package --commit /path/to/new/tree me.myname.myapplication/sysarch/version
```

## Known Problems

- The OSTree Repository cannot be initialized onto a filesystem without extended attributes, in
  particular, NFS does not work. As a workaround, you can set the environment variables
  `XDG_DATA_HOME` (system OSTree Repository) and `HOME` (Runtime checkout) to point to some
  directory on a filesystem which has support for extended attributes.
- Only Linux is supported directly. MacOS and Windows users are recommended to virtualize Linux in
  their respective environments. More information about this is in the
  [Wiki](https://github.com/MaRDI4NFDI/maps/wiki/Non-Linux-OSs).


## Contributing

### Style Practices

All code must conform to these settings of pylint and flake8 (enforced by CI):

```bash
pylint --rcfile pylint.toml src/maps
flake8 --max-line-length 100 --ignore=E402 src/maps
```
