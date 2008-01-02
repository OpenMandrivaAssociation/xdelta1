%define version 1.1.4
%define release %mkrel 1
%define name xdelta1

Summary: A binary delta generator
Name:	%{name}
Version: %{version}
Release: %{release}
Source0: http://xdelta.googlecode.com/files/xdelta-%{version}.tar.bz2
URL:	http://xdelta.org
# (fc) 1.1.4-2mdv fix aclocal warning (upstream issue #49)
Patch0:	xdelta-1.1.4-underquoted.patch
License: GPL
Group: File tools
BuildRequires: emacs-bin glib-devel zlib-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%description 
XDelta is a library interface and application program designed to
compute changes between files.  These changes (deltas) are similar to
the output of the "diff" program in that they may be used to store and
transmit only the changes between files.  However, unlike diff, the
output of XDelta is not expressed in a human-readable format--XDelta
can also also apply these deltas to a copy of the original file(s).
XDelta uses a fast, linear algorithm and performs well on both binary
and text files.  XDelta typically outperforms GNU diff in both time
and generated-delta-size, even for plain text files.  XDelta also
includes a simple implementation of the Rsync algorithm and several
advanced features for implementing RCS-like file-archival with.

%package devel
Summary: Static libraries and header files for development with XDelta
Group: Development/C
Requires: %{name}

%description devel
This package contains the static libraries and header files
required to develop applications using Xdelta.

%prep
%setup -q -n xdelta-%{version}
%patch0 -p1 -b .underquoted

%build
%ifarch alpha
automake
%endif

%configure2_5x --disable-shared
%make all
cd libedsio 
emacs -batch -q -f batch-byte-compile edsio.el

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp
%makeinstall
install -m 644 libedsio/{edsio.el,edsio.elc} \
	$RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp

%multiarch_binaries $RPM_BUILD_ROOT%{_bindir}/xdelta-config

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS COPYING NEWS README
%_bindir/xdelta
%_datadir/aclocal/*
%_mandir/man1/*
%_datadir/emacs/site-lisp/*

%files devel
%defattr(-,root,root)
%_bindir/xdelta-config
%multiarch %{multiarch_bindir}/xdelta-config
%_includedir/*
%_libdir/*
