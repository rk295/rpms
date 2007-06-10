%define name daemontools
%define version 0.76
%define release 1
%define group System Environment/Daemons

Name:		%{name}
Summary: 	Dan Bernstiens Daemon manager
Version:	%{version}
Release:	%{release}.%{dist}
License: 	Copyright 2000 D. J. Bernstein <djb@pobox.com>
Group:		%{group}
Source:		http://cr.yp.to/daemontools/daemontools-0.76.tar.gz
URL:		http://cr.yp.to/daemontools.html
Packager: 	Hildebrand Ops <ops@hildebrand.co.uk>
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-root

Patch: 		daemontools-0.76.errno.patch

%description
Daemontools allows you to easily manage system services.
It runs your services on boot, passes them the correct
environment variables, backgrounds them, respawns them.
It also allows you to easily start, stop, restart, and
check the status of your services.

%prep
%setup -q -n admin/%{name}-%{version}
%patch -p1

%build
./package/compile

%install
%{__mkdir} -p	$RPM_BUILD_ROOT/service
%{__mkdir} -p	$RPM_BUILD_ROOT/usr/bin
%{__cp} ./command/*	$RPM_BUILD_ROOT/usr/bin

%post
if grep svscanboot /etc/inittab >/dev/null
then
  echo 'inittab contains an svscanboot line. I assume that svscan is already running.'
else
  echo 'Adding svscanboot to inittab...'
  %{__rm} -f /etc/inittab'{new}'
  %{__cat} /etc/inittab > /etc/inittab'{new}'
  echo "" >> /etc/inittab'{new}'
  echo "SV:123456:respawn:/usr/bin/svscanboot" >> /etc/inittab'{new}'
  %{__mv} -f /etc/inittab'{new}' /etc/inittab
  kill -HUP 1
  echo 'init should start svscan now.'
fi


%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%attr(750,root,root) %dir /service
/usr/bin/envdir
/usr/bin/envuidgid
/usr/bin/fghack
/usr/bin/multilog
/usr/bin/pgrphack
/usr/bin/readproctitle
/usr/bin/setlock
/usr/bin/setuidgid
/usr/bin/softlimit
/usr/bin/supervise
/usr/bin/svc
/usr/bin/svok
/usr/bin/svscan
/usr/bin/svscanboot
/usr/bin/svstat
/usr/bin/tai64n
/usr/bin/tai64nlocal

%changelog

* Sun Jun 10 2007 Robin Kearney <robin@riviera.org.uk>
- Modded Release line so it is not hilde specific

