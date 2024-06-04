#!/bin/bash

rpmdev-setuptree

cd "$HOME/rpmbuild"

git clone "https://github.com/aaruni96/maps"

VERSION=$(cat maps/Readme.md | grep -i 'version' | head -n 1 | sed 's/^.*version-//' | sed 's/-.*//').0.1

mv maps maps-$VERSION

cd "$HOME/rpmbuild/maps-$VERSION"

# figure out changelogs later
#git log --format="* %ad %an - %s%b%n" $(git rev-list --tags --max-count=1)..HEAD >> pkg/rpm/maps.spec

cd "$HOME/rpmbuild"

tar -czf maps-$VERSION.tar.gz maps-$VERSION

mv maps-$VERSION.tar.gz SOURCES

cp maps-$VERSION/pkg/rpm/maps.spec SPECS/maps.spec

rpmbuild -bb ~/rpmbuild/SPECS/maps.spec
