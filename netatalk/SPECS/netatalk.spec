%define initdir /etc/rc.d/init.d
%define name netatalk
%define version 2.0.5
%define release 2
%define group System Environment/Daemons

Summary: AppleTalk networking programs
Name:    %{name}
Version: %{version}
Release: %{release}.%{?dist}
Epoch:   4
License: GPL
Group: 	 %{group}
Source0: http://download.sourceforge.net/netatalk/netatalk-%{version}.tar.gz
Url:	 http://netatalk.sourceforge.net/
Prereq:  /sbin/chkconfig, /sbin/service 
Requires: pam >= 0.56, /etc/pam.d/system-auth, tcp_wrappers, openssl, cracklib openslp
BuildRequires: cracklib openssl-devel pam quota libtool automake autoconf db4-devel pam-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
This package enables Linux to talk to Macintosh computers via the
AppleTalk networking protocol. It includes a daemon to allow Linux
to act as a file server over EtherTalk or IP for Mac's.

%package devel
Summary: Headers and static libraries for Appletalk development
Group: Development/Libraries

%description devel
This package contains the header files, and static libraries for building
Appletalk networking programs.

%prep
%setup -q

ln -s ./NEWS ChangeLog

%build
touch AUTHORS
%configure --enable-redhat
%{__make} all

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}

# Dont need these and they create a false dependancy on /usr/bin/rc
%{__rm} -f %{buildroot}/usr/share/doc/netatalk-2.0.5/acleandir.rc
%{__rm} -f %{buildroot}/usr/share/man/man1/acleandir.1.gz
%{__rm} -f %{buildroot}/usr/bin/acleandir.rc

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add atalk

%preun
if [ "$1" = "0" ] ; then
  /sbin/service atalk stop > /dev/null 2>&1
  /sbin/chkconfig --del atalk
fi

%postun
if [ "$1" -ge "1" ]; then
  /sbin/service atalk condrestart > /dev/null 2>&1 || :
fi

%files
%defattr(-,root,root)
%doc COPYRIGHT ChangeLog README* TODO VERSION NEWS 
%doc doc
%attr(755,root,root) %config %{initdir}/atalk
%config(noreplace) /etc/netatalk/AppleVolumes.default
%config(noreplace) /etc/netatalk/AppleVolumes.system
%config(noreplace) /etc/netatalk/afpd.conf
%config(noreplace) /etc/netatalk/papd.conf
%config(noreplace) /etc/pam.d/netatalk
%config(noreplace) /etc/netatalk/uams/*
%config(noreplace) /etc/netatalk/atalkd.conf
%config(noreplace) /etc/netatalk/netatalk.conf
%{_sbindir}/*
%{_bindir}/*
%{_mandir}/man*/*
%{_datadir}/netatalk
%{_libdir}/libatalk.a
%{_libdir}/libatalk.la*
%{_libexecdir}/*

%files devel
%defattr(-,root,root)
%dir %{_includedir}/atalk
%{_libdir}/*.a
%{_libdir}/*.la
%attr(0644,root,root) %{_includedir}/atalk/*
%attr(0644,root,root) %{_includedir}/netatalk/*
%{_datadir}/aclocal/netatalk.m4

%changelog
* Fri Mar 4 2011 Robin Kearney <robin@riviera.org.uk> 2
- Fixed dependancy problem on /usr/bin/rc by removing acleandir.[1|rc]

* Thu Mar 3 2011 Robin Kearney <robin@riviera.org.uk> 1
- Initial Build from a new spec file

