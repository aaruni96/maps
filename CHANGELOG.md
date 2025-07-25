# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project tries to adhere to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Upcoming]

### Added
- Added `--export-url`, which generates a valid URL which can be shared to deploy and run a runtime.

### Changed
- Bugfix: Fix a regression where we stopped using overlays
- Bugfix: Fix a regression where we stopped passing through `$HOME/Public`

### Removed

## [0.5]

### Added

- Set value of TERM to something included in the runtime. This can be overridden by the env var
  SANDBOX_TERM.
- Added a `--no-gui` flag to explicitly disable support for GUI applications.
- Added a `--gui` flag to force enable support for GUI applications
- Allow running and deploying runtimes from URL.
- Added optional telemetry. This is **OPT-IN**, and shares limited data. Only the following data is
  transmitted, only when a new runtime is downloaded :
  - the name of the remote repository
  - the URL of the remote repository without username and password
  - the name of the runtime being downloaded

  The telemetry target can be overridden using the environment variable `TELETARGET`.
  
  If telemetry consent was previously given and wishes to be withdrawn, you can set the environment
  variable `MAPS_NOTELE` to any non blank value.
  
  If telemetry consent was previously denied and wishes to be given, you can set the environment
  variable `MAPS_TELEMETRY_CONSENT` to any non blank value.

### Changed

- Bugfix: Fix info message about runtime updates.
- Bugfix: Add whitespace to runtime prompt.
- Changed GUI mounts to attempt binding, with silently continuing on failure, by
  default. Use `--gui` to error if GUI mounts fail.

## [0.4] - 2025-03-13

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
- Bugfix: Fixed a regression which broke running of local runtimes.
- Use default maps upload server
- Improve upload subroutines
- Stop ignoring signals in sandbox

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
