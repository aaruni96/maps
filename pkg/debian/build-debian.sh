#!/bin/bash
# step 1: grab the thingy

#wget 'https://github.com/aaruni96/maps/archive/refs/tags/v0.1.tar.gz' -O maps.tar.gz

#Tar the thingy

OWD=$(pwd)
cd ..
tar -czf /tmp/maps.tar.gz $OWD

#go to tempdir

cd $(mktemp -d)
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

echo "maps (0.1-2) UNRELEASED; urgency=medium

  * Update to v0.1

  * Initial release.

 -- Aaruni Kaushik  <akaushik@mathematik.uni-kl.de>  $(date +'%a, %d %b %Y %H:%M:%S %z')" > "debian/changelog"

# add control

echo 'Source: maps
Maintainer: Aaruni Kaushik <akaushik@mathematik.uni-kl.de>
Section: misc
Priority: optional
Standards-Version: 4.6.0.1
Build-Depends: debhelper-compat (= 13)

Package: maps
Architecture: amd64
Depends: ${shlibs:Depends}, ${misc:Depends}, libcairo2-dev, git, gcc (>= 11), python3, python3-dev, libgirepository1.0-dev, libostree-dev, fuse-overlayfs, python3-venv, libcap-dev, autoconf, python3-gi, python3-tomli
Description: Mathematical Packaging System
 MaPS helps mathematicians create and publish software runtimes, 
 as well as deploy and run software inside published runtimes.' > "debian/control"

# add copyright

echo 'Format: http://dep.debian.net/deps/dep5
Upstream-Name: MaPS
Source: https://github.com/aaruni96/maps

Files: *
Copyright: 2024 Aaruni Kaushi
License: GPL-3.0

License: GPL-3.0
 This package is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 3 of the License, or
 (at your option) any later version.
 .
 This package is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 .
 You should have received a copy of the GNU General Public License
 along with this package; if not, write to the Free Software
 Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA
 .
 On Debian systems, the complete text of the GNU General
 Public License can be found in `/usr/share/common-licenses/GPL-3.`' > "debian/copyright"

# debian.dirs

echo "usr/bin
usr/share/bash-completion/completions" > "debian/maps.dirs"

# debian rules

echo '#!/usr/bin/make -f
%:
	dh $@

override_dh_auto_install:
	$(MAKE) DESTDIR=$$(pwd)/debian/maps prefix=/usr install' > "debian/rules"

# try building, see what happens

debuild -us -uc
