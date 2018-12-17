Name:           bear
Version:        2.3.13
Release:        2%{?dist}
Summary:        Tool that generates a compilation database for clang tooling

License:        GPLv3+
URL:            https://github.com/rizsotto/%{name}
Source:         %{URL}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  clang
BuildRequires:  python%{python3_pkgversion}-devel
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
%make_build

%install
%make_install

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
make check
%endif


%files
%{_bindir}/bear
%{_mandir}/man1/bear.1*

%{_libdir}/bear/

# rpmbuild on RHEL won't automatically pick up ChangeLog.md & README.md
%if 0%{?rhel}
%{_datadir}/doc/bear
%endif

%license COPYING
%doc ChangeLog.md README.md

%changelog
* Sat Nov 24 2018 Dan Čermák <dan.cermak@cgc-instruments.de> - 2.3.13-2
- Implement suggestions from Robert-André Mauchin and Till Hofmann

* Fri Oct  5 2018 Dan Čermák <dan.cermak@cgc-instruments.de> - 2.3.13-1
- Bump version to 2.3.13

* Tue Apr 10 2018 Dan Čermák <dan.cermak@cgc-instruments.de> 2.3.11-1
- Bump version to 2.3.11

* Thu Sep 03 2015 Pavel Odvody <podvody@redhat.com> 2.1.2-1.git15f4447
- new package built with tito
