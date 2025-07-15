Name:           python3-tuspy
Version:        1.1.0
Release:        1%{?dist}
Summary:        A Python client for the tus resumable upload protocol
BuildArch:      noarch

License:        MIT
URL:            https://github.com/tus/tus-py-client
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

Requires:       git python3 python3-aiohttp python3-requests python3-tinydb
BuildRequires:  python3-devel python3-setuptools

%description
tus-py-client is a Python client for uploading files using the tus protocol to any remote server supporting it.

%prep
%autosetup -p1 -n tus-py-client-%{version}

%build
%py3_build

%install
rm -rf $RPM_BUILD_ROOT
%py3_install

%files -n python%{python3_pkgversion}-tuspy
%{python3_sitelib}/tusclient/
%{python3_sitelib}/tuspy-*.egg-info/

%changelog
* Thu Mar 20 2025 Aaruni Kaushik <aaruni@edufor.me> 1.1.0-1
- Initial release
