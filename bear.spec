# https://github.com/j-jorge/bear/commit/ac6be8bebf35cd1a4d4151773707c9ee313b154e
%global commit0 ac6be8bebf35cd1a4d4151773707c9ee313b154e
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Name:           bear
Version:        0.7.0
Release:        0.7git%{shortcommit0}%{?dist}
Summary:        Game engine and editors dedicated to creating great 2D games
License:        GPLv3+ and CC-BY-SA 
URL:            https://github.com/j-jorge/bear
Source0:        https://github.com/j-jorge/bear/archive/%{commit0}/%{name}-%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz

BuildRequires:  boost-devel
BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  docbook-utils
BuildRequires:  gettext
BuildRequires:  libclaw-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(SDL2_mixer)
BuildRequires:  wxGTK-devel
BuildConflicts: wxGTK3-devel

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
# convert docbook2man filename taken from .sgml file to lowercase
sed -i 's|<refentrytitle>\(.*\)</refentrytitle>|<refentrytitle>\L\1</refentrytitle>|' bear-*/desktop/man/*.sgml

# delete glew code because it picks up BSD license
rm -rf bear-engine/core/src/visual/glew/

%build
%cmake -DBEAR_ENGINE_INSTALL_LIBRARY_DIR=%{_lib}/%{name} \
       -DBEAR_FACTORY_INSTALL_LIBRARY_DIR=%{_lib}/%{name} \
       -DCMAKE_SKIP_RPATH:BOOL=ON \
       -DBEAR_USES_FREEDESKTOP=ON \
       -DBEAR_EDITORS_ENABLED=ON
%make_build

%install
%make_install

%find_lang %{name}-engine
%find_lang %{name}-factory

install -d %{buildroot}%{_sysconfdir}/ld.so.conf.d
cat << EOF > %{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}-engine-%{_arch}.conf
%{_libdir}/%{name}
EOF
cat << EOF > %{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}-factory-%{_arch}.conf
%{_libdir}/%{name}
EOF

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

%post factory
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :

%postun factory
/usr/bin/update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ]; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans factory
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files engine -f %{name}-engine.lang
%doc README.md
%license LICENSE license/CCPL license/GPL
%{_libdir}/%{name}
%exclude %{_libdir}/%{name}/lib%{name}-editor.so
%{_mandir}/man6/running-%{name}.6*
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/%{name}-engine-%{_arch}.conf

%files factory -f %{name}-factory.lang
%doc README.md
%license LICENSE license/CCPL license/GPL
%{_bindir}/bend-image
%{_bindir}/image-cutter
%{_bindir}/bf*editor
%{_libdir}/%{name}/lib%{name}-editor.so
%{_datadir}/%{name}-factory
%{_datadir}/applications/bf*editor.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}-factory.png
%{_mandir}/man1/bf*editor.1*
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/%{name}-factory-%{_arch}.conf

%files devel
%doc README.md
%{_includedir}/%{name}
%{_datadir}/cmake/%{name}-engine


%changelog
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
