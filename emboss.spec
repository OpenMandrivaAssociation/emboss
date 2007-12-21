%define name	emboss
%define NAME	EMBOSS
%define version 5.0.0
%define release %mkrel 1
%define major	5
%define libname	%mklibname %{name} %{major}
%define develname %mklibname -d %{name}

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	The European Molecular Biology Open Software Suite
Group:		Sciences/Biology
License:	GPL/LGPL
URL:		http://www.emboss.org
Source0:	ftp://emboss.open-bio.org/pub/EMBOSS/%{NAME}-%{version}.tar.bz2
Source1:	%{name}.default.bz2
Requires:	%{libname} = %{version}
BuildRequires:	libx11-devel
BuildRequires:	automake
BuildRequires:  pcre-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}
Obsoletes:	%{NAME}
Provides:	%{NAME}

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
Obsoletes:	lib%{name} < %{version}

%description -n %{libname}
This package contains the library needed to run %{name}.

%package -n %{develname}
Summary:        Development header files for %{name}
Group:          Development/C
Requires:       %{libname} = %{version}
Provides:       lib%{name}-devel = %{version}-%{release}
Obsoletes:	lib%{name}-devel < %{version}

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
mv %{buildroot}%{_bindir}/digest %{buildroot}%{_bindir}/digest-%{name}
#fix avlmap-utils
mv %{buildroot}%{_bindir}/wordcount %{buildroot}%{_bindir}/wordcount-%{name}
#fix libtool files perms
chmod 644  %{buildroot}%{_libdir}/*.la


%clean
rm -rf %{buildroot}

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING FAQ INSTALL LICENSE NEWS README THANKS
%{_bindir}/*
%{_datadir}/EMBOSS
%config(noreplace) %{_sysconfdir}/emboss.default
%config(noreplace) %{_sysconfdir}/profile.d/emboss.*

%files -n %libname
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %develname
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
%{_includedir}/*


