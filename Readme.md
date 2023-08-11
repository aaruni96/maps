# MaPS - MaRDI Packaging System

## Introduction

MaPS, short for MaRDI Packaging System is the working name for the software system created by TA1 **Computer Algebra** for Measure 1.4 **Predefined software environments**. MaPS provides a unified interface both, to package a software inside a functional environment, and to "install" a published predefined software environment onto a computer system in a user friendly way, while still keeping it separate from the computer's host environment.

## Technical Overview

### Packaging Software

In this mode, the user can commit arbitrary trees into an ostree repo, and then publish them. The trees contain everything required by the application to run, as the resulting package will be run inside a user namespace sandbox. The packager is responsible for providing a correct tree, although, we provide a "default" tree (based on the debian docker image) to begin with.

```bash
# Initialise a new tree from a minimal debian base
maps.py --package --initialize /path/to/new/tree

# Start a bash session inside a sandbox
maps.py --package --sandbox /path/to/new/tree

# Commit the tree into ostree repository
maps.py --package --commit /path/to/new/tree me.myname.myapplication/sysarch/version
```
#### ToDo

 - [ ] Submit `me.myname.myapplication/sysarch/version` to a global, official repository for publishing.

### Deploying Software

We deploy software in `$HOME/.var/maps/app-id/`, in directories `live`, `rofs`, and `rwfs`. Ostree repo is checked out in `rofs`, and marked as read only. Then `rwfs` is overlayed on `rofs`, and presented as `live`. This way the user gets a live mutable tree, but the actual ostree repo is left unmodified and can be reverted to.

 1. Check we have an ostree repo somewhere, if not, initialize it.
 1. Make the directories.
 1. Checkout tree from ostree repo.
 1. Mount overlay at runtime, unmount when done.
 1. Provide option to clean out `rwfs`.

## Requirements

Among other things, we depend on ostree, bubblewrap, and overlayfs-fuse.

## Installing

## Style Practices

All code must conform to these settings of pylint and flake8

```bash
pylint -d C0413,C0103 src/maps.py
flake8 --max-line-length 100 --ignore=E402 src/maps.py
```

