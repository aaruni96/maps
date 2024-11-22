# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project tries to adhere to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Upcoming]

### Added

### Changed

 - Bugfix: Fixed a regression (because of native overlayfs' other implications) which broke command
   defined in manifest

### Removed

## [0.3] - 2024-11-17

### Added
 - Include sysfs in the runtime as read-only
 - Add option to upload runtime for publishing
 - Add runtime name validation for commiting and uploading runtimes

### Changed
 - Improved logic for uninstall
 - Bugfix: interruptible downloads
 - Use native overlayfs instead of fuse implementation. Requires Linux kernel 5.11+
 - Improved handling of bwrap as a dependency

### Removed

## [0.2] - 2024-06-20

### Added
 - Add changelog!
 - Add option to update runtime
 - Add CI scripts to build release packages

### Changed
 - Build bubblewrap using meson/ninja
 - Suppress mkdir error except in Verbose
 - Suppress bubblewrap compilation except in Verbose
 - Handle edge case of live already being mounted
 - Use `umount` instead of `fusermount` to unmount live

### Changed

## [0.1] - 2024-02-12

### New
 - BASH Completion script
 - Add License
 - Preliminary work for building deb packages
 - Spinner to indicate download activity

### Changed
 - UI rewrite
 - Fix --version flag
 - Nicer location for bubblewrap
 - Renamed script to maps from maps.py
 - Uninstalling runtimes now frees up disk space
 - Change invocation of bubblewrap to keep up with changes in bubblewrap


## [0.1-alpha] - 2023-11-22

### Added
 - Initial release!
