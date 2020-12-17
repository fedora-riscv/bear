Name:           bear
Version:        2.4.4
Release:        1%{?dist}
Summary:        Tool that generates a compilation database for clang tooling

License:        GPLv3+
URL:            https://github.com/rizsotto/%{name}
Source:         %{URL}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  clang
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires: make
# python3-lit is only needed for the tests which we only run on Fedora
%{?fedora:BuildRequires: python3-lit}

%description
Build ear produces compilation database in JSON format. This database describes
how single compilation unit should be processed and can be used by Clang
tooling.

%prep
%autosetup -n Bear-%{version}


%build
%cmake .
%cmake_build

%install
%cmake_install

# Fix shebang line
for f in %{buildroot}/%{_bindir}/* ; do
    sed -i.orig "s:^#\!/usr/bin/env\s\+python\s\?$:#!%{__python3}:" $f
    touch -r $f.orig $f
    rm $f.orig
done

# remove twice installed license
rm %{buildroot}/%{_datadir}/doc/bear/COPYING

# Tests fail on EPEL, only run them on Fedora
%if 0%{?fedora}
%check
make check -C %{_vpath_builddir}
%endif


%files
%{_bindir}/bear
%{_datadir}/bash-completion/completions/bear
%{_mandir}/man1/bear.1*

%{_libdir}/bear/

# rpmbuild on RHEL won't automatically pick up ChangeLog.md & README.md
%if 0%{?rhel}
%{_datadir}/doc/bear
%endif

%license COPYING
%doc ChangeLog.md README.md

%changelog
* Sun Sep 13 2020 Dan Čermák <dan.cermak@cgc-instruments.com> - 2.4.4-1
- New upstream release 2.4.4 (rhbz#1877901)

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 26 2020 Dan Čermák <dan.cermak@cgc-instruments.com> - 2.4.3-1
- Bump version to 2.4.3

* Sun Sep  8 2019 Dan Čermák <dan.cermak@cgc-instruments.com> - 2.4.2-1
- Bump version to 2.4.2

* Wed Jul 31 2019 Wolfgang Stöggl <c72578@yahoo.de> - 2.4.1-1
- Bump version to 2.4.1
- Add %%{_datadir}/bash-completion/completions/bear to %%files

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue May 14 2019 Dan Čermák <dan.cermak@cgc-instruments.de> - 2.4.0-1
- Bump version to 2.4.0

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 25 2019 Jonathan Wakely <jwakely@redhat.com> - 2.3.13-3
- Rebuilt for Boost 1.69

* Sat Nov 24 2018 Dan Čermák <dan.cermak@cgc-instruments.de> - 2.3.13-2
- Implement suggestions from Robert-André Mauchin and Till Hofmann

* Fri Oct  5 2018 Dan Čermák <dan.cermak@cgc-instruments.de> - 2.3.13-1
- Bump version to 2.3.13

* Tue Apr 10 2018 Dan Čermák <dan.cermak@cgc-instruments.de> 2.3.11-1
- Bump version to 2.3.11

* Thu Sep 03 2015 Pavel Odvody <podvody@redhat.com> 2.1.2-1.git15f4447
- new package built with tito
