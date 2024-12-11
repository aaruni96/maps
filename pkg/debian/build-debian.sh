#!/bin/bash
# step 1: grab the thingy

#wget 'https://github.com/aaruni96/maps/archive/refs/tags/v0.1.tar.gz' -O maps.tar.gz

#Tar the thingy

OWD=$(pwd | sed "s/^.*\///") 
cd ..
tar -czf /tmp/maps.tar.gz $OWD

#go to tempdir

mkdir -p /tmp/maps-build-temp
cd /tmp/maps-build-temp
mv /tmp/maps.tar.gz ./

# unpack

tar -xf maps.tar.gz

# grab version

VERSION=$(cat maps/Readme.md | grep -i 'version' | head -n 1 | sed 's/^.*version-//' | sed 's/-.*//')

#rename

mv -v maps.tar.gz "maps_${VERSION}.orig.tar.gz"
mv -v "maps" "maps_${VERSION}"

# setup the debian specific dirs

cd "maps_${VERSION}" && mkdir -pv "debian/source"

# add the format version

echo "3.0 (quilt)" > "debian/source/format"

cp -v "pkg/debian/changelog" "debian/changelog"

# add control

cp -v "pkg/debian/control" "debian/control"

# add copyright

cp -v "pkg/debian/copyright" "debian/copyright"

# debian.dirs
cp -v "pkg/debian/maps.dirs" "debian/maps.dirs"

# debian rules

cp -v "pkg/debian/rules" "debian/rules"

# postinst

cp -v "pkg/debian/postinst" "debian/postinst"

# try building, see what happens

debuild -us -uc
