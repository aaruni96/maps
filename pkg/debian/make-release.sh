#!/bin/sh
set -e

do_hash() {
    HASH_NAME=$1
    HASH_CMD=$2
    echo "${HASH_NAME}:"
    for f in $(find -type f); do
        f=$(echo $f | cut -c3-) # remove ./ prefix
        if [ "$f" = "Release" ]; then
            continue
        fi
        echo " $(${HASH_CMD} ${f}  | cut -d" " -f1) $(wc -c $f)"
    done
}

cat << EOF
Origin: RPTU Testing Repository
Label: RPTU
Suite: stable
Codename: stable
Version: 1.0
Architectures: amd64 arm64 arm7 i386
Components: main
Description: Repo for experimental software made in RPTU Kaiserslauatern
Date: $(date -Ru)
EOF
do_hash "MD5Sum" "md5sum"
do_hash "SHA1" "sha1sum"
do_hash "SHA256" "sha256sum"

# Remember to also run 
# dpkg-scanpackages --arch amd64 pool