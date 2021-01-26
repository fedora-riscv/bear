Name:           bear
Version:        3.0.7
Release:        2%{?dist}
Summary:        Tool that generates a compilation database for clang tooling

License:        GPLv3+
URL:            https://github.com/rizsotto/%{name}
Source:         %{URL}/archive/%{version}/%{name}-%{version}.tar.gz
Patch0:         bear.missing-includes.patch
# https://github.com/rizsotto/Bear/pull/348
Patch1:         bear.libexec-subdir.patch

BuildRequires:  cmake
BuildRequires:  cmake(fmt)
BuildRequires:  cmake(gtest)
BuildRequires:  cmake(nlohmann_json)
BuildRequires:  cmake(spdlog)
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gmock-devel
BuildRequires:  grpc-plugins
BuildRequires:  make
BuildRequires:  pkgconfig(grpc)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  python3

# Needed for (disabled) functional tests
#BuildRequires:  python3dist(lit)

%description
Build ear produces compilation database in JSON format. This database describes
how single compilation unit should be processed and can be used by Clang
tooling.

%prep
%autosetup -p 1 -n Bear-%{version}


%build
# Functional tests are broken for some unknown reason, disable for now.
%cmake -DENABLE_FUNC_TESTS=OFF
%cmake_build

%install
%cmake_install

mv %{buildroot}/%{_docdir}/Bear %{buildroot}/%{_docdir}/bear

%check
# Tests run as part of build, because it's the same build target.
# There is no check target.


%files
%{_bindir}/bear
%{_bindir}/citnames
%{_bindir}/intercept
%{_libexecdir}/bear/er
%{_libexecdir}/bear/libexec.so
%{_libexecdir}/bear/wrapper
%{_libexecdir}/bear/wrapper.d
%{_mandir}/man1/bear.1*
%{_mandir}/man1/citnames.1*
%{_mandir}/man1/intercept.1*

# rpmbuild on RHEL won't automatically pick up ChangeLog.md & README.md
%if 0%{?rhel}
%{_datadir}/doc/bear
%endif

%license COPYING
%doc %{_docdir}/bear

%changelog
* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Jan 24 2021 Till Hofmann <thofmann@fedoraproject.org> - 3.0.7-1
- Update to 3.0.7

* Wed Dec 30 11:58:35 CET 2020 Till Hofmann <thofmann@fedoraproject.org> - 3.0.6-1
- Update to 3.0.6

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
