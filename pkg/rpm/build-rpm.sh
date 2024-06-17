#!/bin/bash

set -e

MAPSDIR=$(pwd)

echo "Setting up rpmbuild dir"
mkdir -pv $HOME/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}

echo "cd to rpmbuild"
cd "$HOME/rpmbuild"
ls

mv -v $MAPSDIR ./
ls 

VERSION=$(cat maps/Readme.md | grep -i 'version' | head -n 1 | sed 's/^.*version-//' | sed 's/-.*//').0.1

echo "VERSION is $VERSION"

mv maps maps-$VERSION

#cd "$HOME/rpmbuild/maps-$VERSION"

# figure out changelogs later
#git log --format="* %ad %an - %s%b%n" $(git rev-list --tags --max-count=1)..HEAD >> pkg/rpm/maps.spec

#cd "$HOME/rpmbuild"

tar -czf maps-$VERSION.tar.gz maps-$VERSION

mv maps-$VERSION.tar.gz SOURCES

echo "trying to move SPECfile to right place"
echo "step1 : list specfile"
ls "maps-$VERSION"
ls "maps-$VERSION/pkg"
ls "maps-$VERSION/pkg/rpm"
cp -v maps-$VERSION/pkg/rpm/maps.spec SPECS/maps.spec

rpmbuild -bb SPECS/maps.spec

cp -v RPMS/noarch/maps*.rpm /tmp
