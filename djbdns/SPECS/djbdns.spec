%define name djbdns
%define version 1.05
%define release 1
%define group System Environment/Daemons

Name:		%{name}
Summary: 	Domain Name System tools
Version:	%{version}
Release:	%{release}.HIL.%{dist}
License: 	Copyright 2000 D. J. Bernstein <djb@pobox.com>
Group:		%{group}
Source: 	http://cr.yp.to/djbdns/djbdns-%{PACKAGE_VERSION}.tar.gz
URL: 		http://cr.yp.to/djbdns.html
Packager: 	Hildebrand Ops <ops@hildebrand.co.uk>
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

Patch: 		djbdns-1.05.errno.patch

%description
djbdns is a collection of Domain Name System tools.

%changelog

* Mon Dec 12 2005 Robin Kearney <robin@hildebrand.co.uk>
- Added sdb Release tag
- Moved install root to /usr/bin

* Thu Dec 04 2003 John Leach <john@johnleach.co.uk>
- Added glibc 2.3 errno patch

* Mon Feb 12 2001 Bruce Guenter <bruceg@em.ca>
- Updated to version 1.05

* Mon Jan 22 2001 Bruce Guenter <bruceg@em.ca>
- Updated to version 1.04

* Sun Jan 7 2001 Bruce Guenter <bruceg@em.ca>
- Updated to version 1.03

* Wed Oct 18 2000 Bruce Guenter <bruceg@em.ca>
- Renamed to djbdns.
- Updated to version 1.02

* Thu Mar 30 2000 Bruce Guenter <bruceg@em.ca>
- Moved all the RedHat specific stuff into a seperate "run" package.

* Wed Mar 29 2000 Bruce Guenter <bruceg@em.ca>
- Make the original conf programs retain their original names, and give
  the new programs the name *-rhconf.

* Sun Mar 26 2000 Bruce Guenter <bruceg@em.ca>
- Updated to version 1.00.

* Wed Mar 15 2000 Bruce Guenter <bruceg@em.ca>
- Updated to version 0.93.

* Mon Mar 6 2000 Bruce Guenter <bruceg@em.ca>
- Fixed a typo in the common init script.

* Thu Mar 2 2000 Bruce Guenter <bruceg@em.ca>
- Updated to version 0.91.
- Modified RPM specific files to use new directory structure.
- Added descriptions to the init.d scripts to fix problems with
  chkconfig.

* Sun Feb 20 2000 Bruce Guenter <bruceg@em.ca>
- Fixed some bugs in the init scripts and the redhat-conf script.
- Repackaged the RPM specific stuff into a seperate tarball.

* Tue Feb 15 2000 Bruce Guenter <bruceg@em.ca>
- Added init scripts to start any axfrdns, dnscache, pickdns, rbldns,
  tinydns, or walldns service.

* Mon Feb 14 2000 Bruce Guenter <bruceg@em.ca>
- Added RedHat specific *-conf script to put the log files in /var/log
- Added dnsip to list of programs in /usr/bin


%prep
%setup

# Errno glibc fix patch
%patch -p1 

%build
%{__make}

%install
%{__rm} -fr $RPM_BUILD_ROOT
%{__mkdir} -p $RPM_BUILD_ROOT/{usr,etc}
echo "$RPM_BUILD_ROOT/usr" >conf-home
%{__rm} -f auto_home.o auto_home.c hier.o install instcheck
%{__perl} -pi -le 's!/!'$RPM_BUILD_ROOT'!' hier.c
%{__make} install instcheck
./install
./instcheck

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/usr/bin/*
/etc/*
