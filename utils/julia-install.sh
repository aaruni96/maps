#!/bin/bash

#download Julia, into a directory named `julia`
export FAKEROOTDONTTRYCHOWN=1
fakeroot apt update
fakeroot apt install curl g++ wget
install -dv /etc/julia
install -dv /usr/include/julia
install -dv /usr/include/julia/uv
install -dv /usr/lib/julia
install -dv /usr/libexec/julia
install -dv /usr/share/appdata
install -dv /usr/share/applications
install -dv /usr/share/doc/julia/html/en
install -dv /usr/share/julia
install -dv /usr/share/man/man1
install -v julia/bin/julia /bin/julia
install -v julia/etc/julia/startup.jl /etc/julia/startup.jl
install -v julia/include/julia/* /usr/include/julia/
install -v julia/include/julia/uv/* /usr/include/julia/uv/
install -v julia/lib/* /usr/lib/
install -v julia/lib/julia/* /usr/lib/julia/
install -v julia/libexec/julia/* /usr/libexec/julia/
install -v julia/share/appdata/julia.appdata.xml /usr/share/appdata/
install -v julia/share/applications/julia.desktop /usr/share/applications/
install -v julia/share/man/man1/julia.1 /usr/share/man/man1/julia.1
cp -rv julia/share/doc/julia/html/en/* /usr/share/doc/julia/html/en/
cp -rv julia/share/julia/* /usr/share/julia/
rm -rf julia