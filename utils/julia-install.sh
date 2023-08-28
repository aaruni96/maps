#!/bin/bash

#download Julia
apt install curl g++
apt install -f
curl -sL 'https://julialang-s3.julialang.org/bin/linux/x64/1.9/julia-1.9.2-linux-x86_64.tar.gz' > 'julia-1.9.2-linux-x86_64.tar.gz'
tar --no-same-owner -xvzf julia-1.9.2-linux-x86_64.tar.gz
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
install -v julia-1.9.2/bin/julia /bin/julia
install -v julia-1.9.2/etc/julia/startup.jl /etc/julia/startup.jl
install -v julia-1.9.2/include/julia/* /usr/include/julia/
install -v julia-1.9.2/include/julia/uv/* /usr/include/julia/uv/
install -v julia-1.9.2/lib/* /usr/lib/
install -v julia-1.9.2/lib/julia/* /usr/lib/julia/
install -v julia-1.9.2/libexec/julia/* /usr/libexec/julia/
install -v julia-1.9.2/share/appdata/julia.appdata.xml /usr/share/appdata/
install -v julia-1.9.2/share/applications/julia.desktop /usr/share/applications/
install -v julia-1.9.2/share/man/man1/julia.1 /usr/share/man/man1/julia.1
cp -rv julia-1.9.2/share/doc/julia/html/en/* /usr/share/doc/julia/html/en/
cp -rv julia-1.9.2/share/julia/* /usr/share/julia/
rm -rvf julia-1.9.2 julia-1.9.2-linux-x86_64.tar.gz
