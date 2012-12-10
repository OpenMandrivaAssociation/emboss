%define NAME	EMBOSS
%define major	6
%define libname	%mklibname %{name} %{major}
%define develname %mklibname -d %{name}
%define _disable_ld_no_undefined 1
%define _disable_ld_as_needed 1

Name:		emboss
Version:	6.4.0
Release:	2
Summary:	The European Molecular Biology Open Software Suite
Group:		Sciences/Biology
License:	GPL/LGPL
URL:		http://www.emboss.org
Source0:	ftp://emboss.open-bio.org/pub/EMBOSS/%{NAME}-%{version}.tar.gz
Source1:	%{name}.default.bz2
Requires:	%{libname} = %{version}
BuildRequires:	pkgconfig(x11)
BuildRequires:	automake
BuildRequires:  pcre-devel
%rename %{NAME}

%description
EMBOSS is a new, free Open Source software analysis package specially
developed for the needs of the molecular biology (e.g. EMBnet) user community.
The software automatically copes with data in a variety of formats and even
allows transparent retrieval of sequence data from the web. Also, as extensive
libraries are provided with the package, it is a platform to allow other
scientists to develop and release software in true open source spirit.
EMBOSS also integrates a range of currently available packages and tools for
sequence analysis into a seamless whole.

Reference for EMBOSS: Rice,P. Longden,I. and Bleasby,A.
"EMBOSS: The European Molecular Biology Open Software Suite"
Trends in Genetics June 2000, vol 16, No 6. pp.276-277

%package -n %{libname}
Summary:        Main library for %{name}
Group:          System/Libraries
Provides:       lib%{name} = %{version}-%{release}

%description -n %{libname}
This package contains the library needed to run %{name}.

%package -n %{develname}
Summary:        Development header files for %{name}
Group:          Development/C
Requires:       %{libname} = %{version}
Provides:       lib%{name}-devel = %{version}-%{release}

%description -n %{develname}
Libraries, include files and other resources you can use to develop
%{name} applications.

%prep
%setup -q -n %{NAME}-%{version}
aclocal -I m4
automake
bzcat %{SOURCE1} > emboss.default

%build
%configure2_5x --without-java
%make

%install
rm -rf %{buildroot}
%makeinstall_std
# fix perms and conflicts
chmod 755 %{buildroot}%{_bindir}/runJemboss.csh
for file in merger emma yank; do 
	mv %{buildroot}%{_bindir}/$file %{buildroot}%{_bindir}/$file-%{name}
done
# configuration file
install -d -m 755 %{buildroot}%{_sysconfdir}
install -m 644 emboss.default %{buildroot}%{_sysconfdir}
cd %{buildroot}%{_datadir}/EMBOSS && ln -s ../../../etc/emboss.default .
# shell init files
install -d -m 755 %{buildroot}%{_sysconfdir}/profile.d
cat >%{buildroot}%{_sysconfdir}/profile.d/emboss.sh <<EOF
#EMBOSS environment
export PLPLOT_LIB=%{_datadir}/EMBOSS
EOF
cat >%{buildroot}%{_sysconfdir}/profile.d/emboss.csh <<EOF
#EMBOSS environment
setenv PLPLOT_LIB %{_datadir}/EMBOSS
EOF
#remove jemboss
rm -rf %{buildroot}%{_datadir}/EMBOSS/jemboss
#fix nss conflict
#mv %{buildroot}%{_bindir}/digest %{buildroot}%{_bindir}/digest-%{name}
#fix avlmap-utils
mv %{buildroot}%{_bindir}/wordcount %{buildroot}%{_bindir}/wordcount-%{name}
#fix libtool files perms
chmod 644  %{buildroot}%{_libdir}/*.la

%files
%doc AUTHORS ChangeLog COPYING FAQ INSTALL LICENSE NEWS README THANKS
%{_bindir}/*
%{_datadir}/EMBOSS
%config(noreplace) %{_sysconfdir}/emboss.default
%config(noreplace) %{_sysconfdir}/profile.d/emboss.*

%files -n %{libname}
%{_libdir}/*.so.*

%files -n %{develname}
%{_libdir}/*.so
%{_libdir}/*.a
%{_includedir}/*




%changelog
* Fri Dec 16 2011 StÃ©phane TÃ©letchÃ©a <steletch@mandriva.org> 6.4.0-1mdv2012.0
+ Revision: 741730
- Update to release 6.4.0
- Comment digest renaming no more needed (kept for history for the moment)

* Thu Dec 09 2010 Oden Eriksson <oeriksson@mandriva.com> 6.1.0-2mdv2011.0
+ Revision: 618057
- the mass rebuild of 2010.0 packages

* Mon Jul 20 2009 Frederik Himpe <fhimpe@mandriva.org> 6.1.0-1mdv2010.0
+ Revision: 398117
- Update to new version 6.1.0
- Remove format error patch: integrated upstream

* Wed Mar 04 2009 Guillaume Rousse <guillomovitch@mandriva.org> 5.0.0-4mdv2009.1
+ Revision: 348659
- fix format errors
- disable no-undefined and as-needed linker flags, I'm too lazy to fix packages of other maintainers

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Fri Dec 21 2007 Olivier Blin <blino@mandriva.org> 5.0.0-1mdv2008.1
+ Revision: 136403
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Mon Jul 23 2007 Funda Wang <fwang@mandriva.org> 5.0.0-1mdv2008.0
+ Revision: 54565
- New version


* Tue Dec 19 2006 Eric Fernandez <zeb@mandriva.org> 4.0.0-1mdv2007.0
+ Revision: 99559
- Import emboss

* Tue Dec 19 2006 Eric Fernandez <zeb@zebulon.org.uk> 4.0.0-1mdv2007.1
- new release

* Mon Jun 26 2006 Eric Fernandez <zeb@zebulon.org.uk> 3.0.0-2mdv2007.0
- new source url

* Mon Jun 26 2006 Eric Fernandez <zeb@zebulon.org.uk> 3.0.0-1mdv2007.0
- new release

* Mon Apr 03 2006 Guillaume Rousse <guillomovitch@mandriva.org> 2.9.0-6mdk
- various rpmlint fixes

* Mon Apr 03 2006 Guillaume Rousse <guillomovitch@mandriva.org> 2.9.0-5mdk
- fix conflict with package avlmap-utils by renaming /usr/bin/wordcount to /usr/bin/wordcount-emboss

* Fri Oct 07 2005 Nicolas Lécureuil <neoclust@mandriva.org> 2.9.0-4mdk
- Fix BuildRequires
- %%mkrel

* Sun Jun 05 2005 Guillaume Rousse <guillomovitch@mandriva.org> 2.9.0-3mdk 
- fix conflict with package nss by renaming /usr/bin/digest to /usr/bin/digest-emboss

* Fri Jan 28 2005 Guillaume Rousse <guillomovitch@mandrake.org> 2.9.0-2mdk 
- fix pcre conflict (Marc Koschewski <marc@osknowledge.org>)
- remove .c files in /usr/include
- spec cleanup

* Tue Jan 18 2005 Guillaume Rousse <guillomovitch@mandrake.org> 2.9.0-1mdk 
- contributed by Gaëtan Lehmann (gaetan.lehmann@jouy.inra.fr) 
- drop __libtoolize hack
- drop patch0

* Thu Jul 22 2004 Guillaume Rousse <guillomovitch@mandrake.org> 2.8.0-2mdk 
- remove installed java stuff

* Tue Dec 30 2003 Guillaume Rousse <guillomovitch@mandrake.org> 2.8.0-1mdk
- new version
- changed name to emboss, mixed cases sucks
- fixed conflicts
- rediff patch

