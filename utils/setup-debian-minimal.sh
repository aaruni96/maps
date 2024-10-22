#!/bin/bash

#first time setup
#run from maps directory

#get minimal debain image
wget 'https://github.com/debuerreotype/docker-debian-artifacts/raw/dist-amd64/bookworm/rootfs.tar.xz'

#untar
mkdir -pv ../ostree/debian-minimal
cp rootfs.tar.xz ../ostree/debian-minimal/
cd ../ostree/debian-minimal/
tar -xvf rootfs.tar.xz
rm -v rootfs.tar.xz

#comment out apt from passwd
sed -i bak -e 's/^_apt/#_apt/' etc/passwd

#go back to maps directory
cd ../..

#source venv
source .venv/bin/activate

#sandbox into maps, install fakeroot

./src/maps package --sandbox ostree/debian-minimal

