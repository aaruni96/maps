# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project tries to adhere to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Upcoming]

### Added

- Enable support for graphical application.
- Add profile for AppArmor.
- **BREAKING** : Added ability to disambiguate based on remotes. This changes how the files are
  organized on disk. Remove `$HOME/.var/org.mardi.maps` to refresh if you run into problems.
- Added testsuite!

### Changed

- Bugfix: Fixed a regression (because of native overlayfs' other implications) which broke command
  defined in manifest
- Packaging: Fixed packaging for arch based.
- Use `ostree` binary to pull files instead of the `ostree` library. This shows progress on
  downloading files.
- Use `--unshare-uts` to set hostname instead of by hacking an environment variable.
- Bugfix: Fixed a regression which broke running of local runtimes.
- Use default maps upload server
- Improve upload subroutines

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
