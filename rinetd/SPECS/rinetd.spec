%define name rinetd
%define version 0.62
%define release 0.2
%define group Productivity/Networking/System

Name:           %{name}
License:        GPL-2.0+
Group:          %{group}
AutoReqProv:    on
Version:        %{version}
Release:        %{release}.%{dist}
Summary:        TCP Redirection Server
Url:            http://www.boutell.com/rinetd/
Source0:        rinetd-0.62.tar.gz
Source1:        rc.rinetd
Source2:        logrotate.rinetd
Patch0:         rinetd-conf.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
rinetd redirects TCP connections from one IP address and port to
another address and port. rinetd is a single-process server which
handles any number of connections to the address or port pairs
specified in the file /etc/rinetd.conf. Because rinetd runs as a single
process using nonblocking I/O, it is able to redirect a large number of
connections without a severe impact on the machine. This makes it
practical to run TCP services on machines inside an IP masquerading
firewall.

Note: rinetd can not redirect FTP because FTP requires more than one
socket.



Authors:
--------
    Thomas Boutell <boutell@boutell.com>

%prep
%setup
%patch0

%build
make CFLAGS="$RPM_OPT_FLAGS"

%install
mkdir -p $RPM_BUILD_ROOT/%_mandir/man8
mkdir -p $RPM_BUILD_ROOT/etc/init.d
mkdir -p $RPM_BUILD_ROOT/etc/logrotate.d
mkdir -p $RPM_BUILD_ROOT/usr/sbin
touch $RPM_BUILD_ROOT/etc/rinetd.conf
install -m 700 rinetd $RPM_BUILD_ROOT/usr/sbin
install -m 644 rinetd.8 $RPM_BUILD_ROOT%_mandir/man8
install -m 755 $RPM_SOURCE_DIR/rc.rinetd $RPM_BUILD_ROOT/etc/init.d/rinetd
install -m 644 %SOURCE2 $RPM_BUILD_ROOT/etc/logrotate.d/rinetd
ln -s ../../etc/init.d/rinetd $RPM_BUILD_ROOT/usr/sbin/rcrinetd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%doc CHANGES README index.html rinetd.conf.sample
%config(missingok,noreplace) %ghost /etc/rinetd.conf
%config(noreplace) /etc/logrotate.d/rinetd
%config /etc/init.d/rinetd
%_mandir/man8/rinetd.8.gz
/usr/sbin/rcrinetd
/usr/sbin/rinetd

%changelog
* Thu Sep 5 2013 robin@kearney.co.uk
- Initial build with my own spec file
