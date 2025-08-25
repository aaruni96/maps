Name:           maps
Version:        0.7
Release:        1%{?dist}
Summary:        Mathematical Packaging System
BuildArch:      noarch

License:        GPL3
URL:            https://github.com/MaRDI4NFDI/maps
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  xdg-utils
Requires:       git cairo-devel gcc python3-devel gobject-introspection-devel ostree ostree-devel python3-progress libcap-devel cairo-gobject-devel bash-completion python3-tomli python3-tomli-w meson python3-tuspy xdg-utils

%description
MaPS helps mathematicians create and publish software runtimes, as well as deploy and run software inside published runtimes


%prep
%setup -n %{name}-%{version}


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_bindir} $RPM_BUILD_ROOT/%{_datadir}/bash-completion/completions
install -Dm 755 src/%{name} $RPM_BUILD_ROOT/%{_bindir}
install -Dm 644 src/completion.bash $RPM_BUILD_ROOT/%{_datadir}/bash-completion/completions/%{name}
install -Dm 644 src/usr.bin.%{name} $RPM_BUILD_ROOT/%{_sysconfdir}/apparmor.d/usr.bin.%{name}
install -Dm 644 src/%{name}.desktop $RPM_BUILD_ROOT/%{_prefix}/share/applications/%{name}.desktop
xdg-mime default maps.desktop x-scheme-handler/maps


%files
%{_bindir}/%{name}
%{_datadir}/bash-completion/completions/%{name}
%{_sysconfdir}/apparmor.d/usr.bin.%{name}
%{_prefix}/share/applications/%{name}.desktop


%changelog

* Mon Aug 25 2025 Aaruni Kaushik <akaushik@mathamtik.uni-kl.de> 0.7.0.1
- Update to version 0.7

* Sat Jul 26 2025 Aaruni Kaushik <akaushik@mathamtik.uni-kl.de> 0.6.0.1
- Update to version 0.6

* Tue Jul 22 2025 Aaruni Kaushik <akaushik@mathamtik.uni-kl.de> 0.5.0.1
- Update to version 0.5

* Thu Mar 13 2025 Aaruni Kaushik <akaushik@mathematik.uni-kl.de> 0.4.0.1
- Update to version 0.4

* Sun Nov 17 2024 Aaruni Kaushik <akaushik@mathematik.uni-kl.de> 0.3.0.1
- Update to version 0.3

* Fri Jun 21 2024 Aaruni Kaushik <akaushik@mathematik.uni-kl.de> 0.2.0.1
- Update to version 0.2

* Mon Feb 12 2024 Aaruni Kaushk <akaushik@mathematik.uni-kl.de> 0.1.0.2
- Update to version 0.1

* Wed Nov 22 2023 Aaruni Kaushik <akaushik@mathematik.uni-kl.de> 0.1.0.1
- Initial alpha release
