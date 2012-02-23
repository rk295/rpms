%define version 0.3.3
%define release 1

Name:       colortail
Version:	%{version}
Release:	%{release}.%{dist}
Epoch:      0
Summary:    Like tail but can colorize the output

Group:          Development/Libraries
License:        GPL
URL:            http://ftp.psn.ru/debian/pool/main/c/colortail/
Source0:        http://ftp.psn.ru/debian/pool/main/c/colortail/colortail-0.3.3.tar.gz 
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


%description
Colortail works like tail but can optionally read one or more config files
where it's specified which patterns results in which colors.

Colortail uses regular expressions (see regex(7)) to determine which lines and 
parts of lines to print in which colors.

%prep
%setup -q


%build
./configure
%{__make} 


%install
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}

%{__install} -d %{buildroot}%{_bindir}
%{__install} -s %{name} %{buildroot}%{_bindir}/

%{__install} -d %{buildroot}%{_defaultdocdir}/%{name}-%{version}
%{__install} -c -m 755 AUTHORS %{buildroot}%{_defaultdocdir}/%{name}-%{version}/
%{__install} -c -m 755 BUGS %{buildroot}%{_defaultdocdir}/%{name}-%{version}
%{__install} -c -m 755 ChangeLog %{buildroot}%{_defaultdocdir}/%{name}-%{version}
%{__install} -c -m 755 INSTALL %{buildroot}%{_defaultdocdir}/%{name}-%{version}
%{__install} -c -m 755 NEWS %{buildroot}%{_defaultdocdir}/%{name}-%{version}
%{__install} -c -m 755 README %{buildroot}%{_defaultdocdir}/%{name}-%{version}
%{__install} -c -m 755 TODO %{buildroot}%{_defaultdocdir}/%{name}-%{version}

%{__install} -d %{buildroot}%{_defaultdocdir}/%{name}-%{version}/example-conf
%{__install} -c -m 755 example-conf/conf.daemon %{buildroot}%{_defaultdocdir}/%{name}-%{version}/example-conf
%{__install} -c -m 755 example-conf/conf.kernel %{buildroot}%{_defaultdocdir}/%{name}-%{version}/example-conf
%{__install} -c -m 755 example-conf/conf.messages %{buildroot}%{_defaultdocdir}/%{name}-%{version}/example-conf
%{__install} -c -m 755 example-conf/conf.secure %{buildroot}%{_defaultdocdir}/%{name}-%{version}/example-conf
%{__install} -c -m 755 example-conf/conf.xferlog %{buildroot}%{_defaultdocdir}/%{name}-%{version}/example-conf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_bindir}/*
%doc %{_defaultdocdir}/%{name}-%{version}

%changelog
* Thu Feb 23 2012 Robin Kearney
- Initial release
