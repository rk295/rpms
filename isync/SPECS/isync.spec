%define version 1.0.4
%define release 2

Summary: Utility to synchronize IMAP mailboxes with local maildir folders
Name: isync
Version: %{version}
Release: %{release}.%{dist}
License: GPL
Group: Applications/Internet
Source: isync-1.0.4.tar.gz
URL: http://isync.sf.net/
Packager: Oswald Buddenhagen <ossi@users.sf.net>
BuildRoot: /var/tmp/%{name}-buildroot

%description
isync is a command line utility which synchronizes mailboxes; currently
Maildir and IMAP4 mailboxes are supported.
New messages, message deletions and flag changes can be propagated both ways.
It is useful for working in disconnected mode, such as on a laptop or with a
non-permanent internet collection (dIMAP).

%prep
%setup
%build
./configure --prefix=/usr

%install
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc AUTHORS COPYING NEWS README TODO ChangeLog src/mbsyncrc.sample src/compat/isyncrc.sample
/usr/bin/isync
/usr/bin/mbsync
/usr/bin/mdconvert
/usr/bin/get-cert
/usr/share/doc/isync/AUTHORS
/usr/share/doc/isync/ChangeLog
/usr/share/doc/isync/NEWS
/usr/share/doc/isync/README
/usr/share/doc/isync/TODO
/usr/share/man/man1/isync.1.gz
/usr/share/man/man1/mbsync.1.gz
/usr/share/man/man1/mdconvert.1.gz
