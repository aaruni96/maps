Name:           maps
Version:        0.3.0.1
Release:        1%{?dist}
Summary:        Mathematical Packaging System
BuildArch:      noarch

License:        GPL3
URL:            https://github.com/mardi4NFDI/maps
Source0:        %{name}-%{version}.tar.gz

Requires:       git cairo-devel gcc python3-devel gobject-introspection-devel ostree ostree-devel python3-progress libcap-devel autoconf cairo-gobject-devel bash-completion python-tomli meson
#TODO: needs python3-tuspy

%description
MaPS helps mathematicians create and publish software runtimes, as well as deploy and run software inside published runtimes


%prep
%setup -q


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_bindir} $RPM_BUILD_ROOT/%{_datadir}/bash-completion/completions
install -Dm 755 src/%{name} $RPM_BUILD_ROOT/%{_bindir}
install -Dm 644 src/completion.bash $RPM_BUILD_ROOT/%{_datadir}/bash-completion/completions/%{name}
install -Dm 644 src/usr.bin.%{name} $RPM_BUILD_ROOT/%{_sysconfdir}/apparmor.d/usr.bin.%{name}


%files
%{_bindir}/%{name}
%{_datadir}/bash-completion/completions/%{name}
%{_sysconfdir}/apparmor.d/usr.bin.%{name}



%changelog

* Sun Nov 17 2024 Aaruni Kaushik <akaushik@mathematik.uni-kl.de> 0.3.0.1
- Update to version 0.3

* Fri Jun 21 2024 Aaruni Kaushik <akaushik@mathematik.uni-kl.de> 0.2.0.1
- Update to version 0.2

* Mon Feb 12 2024 Aaruni Kaushk <akaushik@mathematik.uni-kl.de> 0.1.0.2
- Update to version 0.1

* Wed Nov 22 2023 Aaruni Kaushik <akaushik@mathematik.uni-kl.de> 0.1.0.1
- Initial alpha release
