%define name ucspi-tcp
%define version 0.88
%define release 1
%define group System Environment/Daemons

Name:		%{name}
Summary: 	Dan Bernstiens TCP superserver
Version:	%{version}
Release:	%{release}.HIL.%{dist}
License: 	Copyright 2000 D. J. Bernstein <djb@pobox.com>
Group:		%{group}
Source:		http://cr.yp.to/ucspi-tcp/ucspi-tcp-%{version}.tar.gz
URL:		http://cr.yp.to/ucspi-tcp.html
Packager: 	Hildebrand Ops <ops@hildebrand.co.uk>
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

Patch0: ucspi-tcp-0.88.errno.patch
Patch1: ucspi-tcp-0.88.a_record.patch
Patch2: ucspi-tcp-0.88.nobase.patch

%description
tcpserver and tcpclient are easy-to-use command-line
tools for building TCP client-server applications.

%prep
%setup -q

# Fixes errno glibc 2.3 bug
%patch0 -p1

%patch1 -p1

# Fixes help message and removes default rbl server
%patch2 -p1

%build
echo $RPM_BUILD_ROOT/usr > conf-home
%{__make}

%install
%{__mkdir} -p $RPM_BUILD_ROOT/usr/bin
%{__make} setup check

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(755,root,root)
/usr/bin/addcr
/usr/bin/argv0
/usr/bin/delcr
/usr/bin/fixcrio
/usr/bin/mconnect
/usr/bin/mconnect-io
/usr/bin/rblsmtpd
/usr/bin/recordio
/usr/bin/tcpcat
/usr/bin/tcpclient
/usr/bin/tcprules
/usr/bin/tcprulescheck
/usr/bin/tcpserver

# sample clients
/usr/bin/date@
/usr/bin/finger@
/usr/bin/http@
/usr/bin/who@

%changelog
