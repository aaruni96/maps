# Documentation for making a release

In short, the following steps need to be followed to make a new MaPS release:

1. Branch off from `devel`
2. Make a PR targeting `devel` which only runs the `bump-version.sh` script. This script needs to be run from the root of the git repository, with the new version number. As an example, to make the release `0.6`, the exact command is :
```bash
bash dev/bump-version.sh 0.6
```
3. Merge this PR to `devel` with the name `Prep release <new-version>`.
4. Create a PR to merge `devel` to `master` with the name `Release <new-version>`.
5. Create a new tag and release in github.
6. Update the relevant files on the Arch Linux User Repo, and Fedora COPR.
