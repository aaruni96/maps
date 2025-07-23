#!/bin/bash

# step 0. bump version in program

escaped_version=$(echo $1 | sed 's/-/--/')

sed -i "s/\(VERSION =\).*$/\1 '${1}'/" src/maps
sed -i "s/badge\/version.*/badge\/version-${escaped_version}-blue\)/" Readme.md
sed -i """8i ## [Upcoming]\n\n### Added\n\n### Changed\n\n### Removed\n""" CHANGELOG.md

if [[ ! $1 =~ "dev" ]]; then
    # step 1. bump versions
    sed -i "s/pkgver=.*/pkgver=${1}/" pkg/arch/PKGBUILD
    sed -i "s/\(Version:\s*\).*$/\1${1}/" pkg/rpm/maps.spec
    sed -i "s/Upcoming/${1}/" CHANGELOG.md


    # step 2. add changelog entries to pkg infra
    # step 2.1. fedora / rpm
    linenumber=$(echo "$(grep -n "%changelog" pkg/rpm/maps.spec | cut -d : -f 1 )+2" | bc)
    rpmentry="""* $(date +"%a %b %d %Y Aaruni Kaushik <akaushik@mathamtik.uni-kl.de> ${1}.0.1")\n- Update to version ${1}"""
    sed -i "${linenumber}i ${rpmentry}\n" pkg/rpm/maps.spec

    # step 2.2. debian/deb
    debdate="""$(date +" -- Aaruni Kaushik <akaushik@mathematik.uni-kl.de> %a, %d %b %Y %H:%M:%S %z")"""
    debentry="""maps (${1}-1) UNRELEASED; urgency=medium\n\n  * Update to v${1}\n\n${debdate}"""
    sed -i "1i $debentry\n" pkg/debian/changelog
fi
