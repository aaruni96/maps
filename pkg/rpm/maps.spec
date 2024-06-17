Name:           maps
Version:        0.1.0.1
Release:        1%{?dist}
Summary:        Mathematical Packaging System
BuildArch:      noarch

License:        GPL3
URL:            https://github.com/mardi4NFDI/maps
Source0:        %{name}-%{version}.tar.gz

Requires:       git cairo-devel gcc python3-devel gobject-introspection-devel ostree-devel fuse-overlayfs libcap-devel autoconf cairo-gobject-devel bash-completion python-tomli

%description
MaPS helps mathematicians create and publish software runtimes, as well as deploy and run software inside published runtimes


%prep
%setup -q


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_bindir} $RPM_BUILD_ROOT/%{_datadir}/bash-completion/completions
cp src/%{name} $RPM_BUILD_ROOT/%{_bindir}
cp src/completion.bash $RPM_BUILD_ROOT/%{_datadir}/bash-completion/completions/%{name}


%files
%{_bindir}/%{name}
%{_datadir}/bash-completion/completions/%{name}



%changelog
