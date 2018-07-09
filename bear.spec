# https://github.com/j-jorge/bear/commit/781ec8022b652b6ba2b76e4385d08c1ef320fcc5
%global commit0 781ec8022b652b6ba2b76e4385d08c1ef320fcc5
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Name:           bear
Version:        0.7.0
Release:        0.20.20161230git%{shortcommit0}%{?dist}
Summary:        Game engine and editors dedicated to creating great 2D games
License:        GPLv3+ and CC-BY-SA 
URL:            https://github.com/j-jorge/bear
Source0:        https://github.com/j-jorge/bear/archive/%{commit0}/%{name}-%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz

# Build is broken on ppc64le 
%if 0%{?fedora} >= 26
ExcludeArch:    ppc64le
%endif

BuildRequires:  gcc-c++
BuildRequires:  boost-devel
BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  docbook-utils
BuildRequires:  gettext
%if 0%{?fedora} >= 26
BuildRequires:  libclaw-devel >= 1.7.4-17
%else
BuildRequires:  libclaw-devel >= 1.7.4-16
%endif
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(SDL2_mixer)
BuildRequires:  wxGTK-devel
BuildConflicts: wxGTK3-devel
Requires:       hicolor-icon-theme


%description
The Bear engine is a set of C++ libraries and tools dedicated to creating
great 2D games. It has been used to create Plee the Bear (plee-the-bear),
Andy's Super Great Park (asgp) and Tunnel (tunnel).

The engine comes with a set of tools, namely the Bear Factory, intended to
help creating resources for the game. These tools include a level editor,
a character/model editor and an animation editor.


%package engine
Summary: Run-time libraries for games based on the Bear engine

%description engine
The Bear engine is a set of C++ libraries and tools dedicated to creating
great 2D games. It has been used to create Plee the Bear (plee-the-bear),
Andy's Super Great Park (asgp) and Tunnel (tunnel).

This package contains the run-time libraries used by the games based on
the Bear engine.


%package factory
Summary: Level, animation and model editors for the Bear engine
Requires: %{name}-engine%{?_isa} = %{version}-%{release}

%description factory
This package includes the level editor, animation editor and model editor
of the Bear Engine for Plee the Bear & Andy's Super Great Park.


%package devel
Summary: Development files for %{name}
Requires: %{name}-engine%{?_isa} = %{version}-%{release}

%description devel
Development files for %{name}

%prep
%setup -qn %{name}-%{commit0}

# change docbook_to_man to docbook2man
sed -i -e 's|docbook-to-man|docbook2man|g' cmake-helper/docbook-to-man.cmake

# delete glew code because it picks up BSD license
rm -rf bear-engine/core/src/visual/glew/

%build
%cmake -DBEAR_ENGINE_INSTALL_LIBRARY_DIR=%{_lib} \
       -DBEAR_FACTORY_INSTALL_LIBRARY_DIR=%{_lib} \
       -DCMAKE_SKIP_RPATH:BOOL=ON \
       -DBEAR_USES_FREEDESKTOP=ON \
       -DRUNNING_BEAR_ENABLED=ON \
       -DBEAR_EDITORS_ENABLED=ON
%make_build

%install
%make_install

%find_lang %{name}-engine
%find_lang %{name}-factory

# copy devel files for subpkg bear-devel
install -dm 755 %{buildroot}%{_includedir}/%{name}/cmake-helper/
install -D cmake-helper/{*.cmake,*.cmake.in} %{buildroot}%{_includedir}/%{name}/cmake-helper/
for file in $(find bear-engine/{core,lib}/src -name *.hpp -o -name *.tpp);
do
    install -Dm 0644 $file %{buildroot}%{_includedir}/%{name}/$file
done
# fixes E: script-without-shebang
chmod a-x %{buildroot}%{_includedir}/%{name}/cmake-helper/*.cmake*

rm -rf %{buildroot}%{_datadir}/pixmaps
rm -rf %{buildroot}%{_datadir}/applications/desc2img.desktop

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop

%post engine -p /sbin/ldconfig
%postun engine -p /sbin/ldconfig

%post factory -p /sbin/ldconfig
%postun factory -p /sbin/ldconfig

%files engine -f %{name}-engine.lang
%doc README.md
%license LICENSE license/CCPL license/GPL
%{_bindir}/running-%{name}
%{_libdir}/lib%{name}_*.so
%exclude %{_libdir}/lib%{name}-editor.so
%{_mandir}/man6/running-%{name}.6*

%files factory -f %{name}-factory.lang
%doc README.md
%license LICENSE license/CCPL license/GPL
%{_bindir}/bend-image
%{_bindir}/image-cutter
%{_bindir}/bf*editor
%{_libdir}/lib%{name}-editor.so
%{_datadir}/%{name}-factory
%{_datadir}/applications/bf*editor.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}-factory.png
%{_mandir}/man1/bf*editor.1*

%files devel
%doc README.md
%{_includedir}/%{name}
%{_datadir}/cmake/%{name}-engine


%changelog
* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-0.20.20161230git781ec80
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 23 2018 Jonathan Wakely <jwakely@redhat.com> - 0.7.0-0.19.20161230git781ec80
- Rebuilt for Boost 1.66

* Sun Jan 07 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.7.0-0.18.20161230git781ec80
- Remove obsolete scriptlets

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-0.17.20161230git781ec80
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-0.16.20161230git781ec80
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Jonathan Wakely <jwakely@redhat.com> - 0.7.0-0.15.20161230git781ec80
- Rebuilt for s390x binutils bug

* Tue Jul 18 2017 Jonathan Wakely <jwakely@redhat.com> - 0.7.0-0.14.20161230git781ec80
- Rebuilt for Boost 1.64

* Wed Feb 01 2017 Martin Gansser <martinkg@fedoraproject.org> - 0.7.0-0.13.20161230git
- rebuild for rawhide, with libclaw-devel >= 1.7.4-17

* Sat Jan 14 2017 Martin Gansser <martinkg@fedoraproject.org> - 0.7.0-0.12.20161230git
- remove %%{name}-engine-%%{_arch}.conf %%{name}-factory-%%{_arch}.conf
- add missing /sbin/ldconfig calls in %%post and %%postun
- add CMAKE option -DRUNNING_BEAR_ENABLED=ON for missing running-bear file
- add %%{_bindir}/running-%%{name} to engine file section
- install engine libraries into -DBEAR_ENGINE_INSTALL_LIBRARY_DIR=%%{_lib}
- install factory libraries into -DBEAR_FACTORY_INSTALL_LIBRARY_DIR=%%{_lib}

* Mon Jan  9 2017 Michael Schwendt <mschwendt@fedoraproject.org> - 0.7.0-0.11.20161230git
- fix Release tag to include snapshot checkout date
- prepare rebuild against libclaw >= 1.7.4-16 for fix ABI compatibility

* Mon Jan 02 2017 Martin Gansser <martinkg@fedoraproject.org> - 0.7.0-0.10git781ec80
- add RR hicolor-icon-theme

* Fri Dec 30 2016 Martin Gansser <martinkg@fedoraproject.org> - 0.7.0-0.9git781ec80
- update to 0.7.0-0.9git781ec80

* Tue Dec 27 2016 Martin Gansser <martinkg@fedoraproject.org> - 0.7.0-0.8gitac6be8b
- add if condition due ppc64le build problem

* Fri Dec 23 2016 Martin Gansser <martinkg@fedoraproject.org> - 0.7.0-0.7gitac6be8b
- change to -DCMAKE_SKIP_RPATH:BOOL=ON
- obsolete chrpath command
- convert docbook2man filename taken from .sgml file to lowercase
- remove BR chrpath

* Tue Dec 13 2016 Martin Gansser <martinkg@fedoraproject.org> - 0.7.0-0.6gitac6be8b
- use wildcard to copy all cmake and cmake.in files for subpkg bear-devel
- copy also *.tpp files for subpkg bear-devel
- fix spurious-executable-perm
- fixes E: script-without-shebang
- specfile cleanup

* Tue Dec 13 2016 Martin Gansser <martinkg@fedoraproject.org> - 0.7.0-0.5gitac6be8b
- Dropped subpkg engine/factory-devel because unversioned files needed at runtime
- Add subpkg %%{name}-devel

* Mon Dec 12 2016 Martin Gansser <martinkg@fedoraproject.org> - 0.7.0-0.4gitac6be8b
- Add Requires: %%{name}-engine%%{?_isa} = %%{version}-%%{release} to bear-factory
- Delete glew code because it picks up BSD license
- run-time is the correct spelling, not runtime
- Add gtk-update-icon-cache in %%postun and %%posttrans section for bear-factory
- Add update-desktop-database in %%post and %%postun section for bear-factory
- Take ownership of %%dir %%{_datadir}/%%{name}-factory/images/
  %%dir %%{_datadir}/%%{name}-factory/item-description/
  %%dir %%{_datadir}/%%{name}-factory//item-description/generic in file section
- Add subpkg engine/factory-devel for unversioned files

* Mon Nov 28 2016 Martin Gansser <martinkg@fedoraproject.org> - 0.7.0-0.3gitac6be8b
- Add BR chrpath
- Add BR libjpeg-turbo-devel
- Add BuildConflicts wxGTK3-devel

* Sun Nov 27 2016 Martin Gansser <martinkg@fedoraproject.org> - 0.7.0-0.2gitac6be8b
- Remove Conflicts: wxGTK3-devel"
- Compressed sed command
- replace (non packaged) with (tunnel) from the descriptions
- replace (andy-super-great-park) with (asgp) from the descriptions
- run-time is the correct spelling, not runtime
- Add %%config to fix the non-conffile-in-etc warnings
- Remove desc2img.desktop due desc2img binary missing

* Sun Nov 27 2016 Martin Gansser <martinkg@fedoraproject.org> - 0.7.0-0.1gitac6be8b
- imported package bear
