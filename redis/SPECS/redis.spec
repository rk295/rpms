%define pid_dir %{_localstatedir}/run/redis
%define pid_file %{pid_dir}/redis.pid

Summary: redis
Name: redis
Version: 2.6.4
Release: 0
License: BSD
Group: Applications/Multimedia
URL: http://code.google.com/p/redis/

Source0: redis-%{version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: gcc, make
Requires(post): /sbin/chkconfig /usr/sbin/useradd
Requires(preun): /sbin/chkconfig, /sbin/service
Requires(postun): /sbin/service
Provides: redis

Packager: William Gregorian <dev-null@will-bloggs-too.com>

%description
Redis is a key-value database. It is similar to memcached but the dataset is
not volatile, and values can be strings, exactly like in memcached, but also
lists and sets with atomic operations to push/pop elements.

In order to be very fast but at the same time persistent the whole dataset is
taken in memory and from time to time and/or when a number of changes to the
dataset are performed it is written asynchronously on disk. You may lose the
last few queries that is acceptable in many applications but it is as fast
as an in memory DB (beta 6 of Redis includes initial support for master-slave
replication in order to solve this problem by redundancy).

Compression and other interesting features are a work in progress. Redis is
written in ANSI C and works in most POSIX systems like Linux, *BSD, Mac OS X,
and so on. Redis is free software released under the very liberal BSD license.

%prep
%setup

%{__cat} <<EOF >redis.logrotate
%{__cat} <<EOF >redis.logrotate
%{_localstatedir}/log/redis/*log {
    missingok
}
EOF

%{__cat} <<'EOF' >redis.sysv
#!/bin/bash
#
# Init file for redis
#
# chkconfig: - 80 12
# description: A persistent key-value database with network interface
# processname: redis-server
# config: /etc/redis.conf
# pidfile: %{pidfile}

source %{_sysconfdir}/init.d/functions

RETVAL=0
prog="redis-server"

start() {
  echo -n $"Starting $prog: "
  daemon --user redis --pidfile %{pid_file} %{_sbindir}/$prog /etc/redis.conf
  RETVAL=$?
  echo
  [ $RETVAL -eq 0 ] && touch %{_localstatedir}/lock/subsys/$prog
  return $RETVAL
}

stop() {
    PID=`cat %{pid_file} 2>/dev/null`
    if [ -n "$PID" ]; then
        echo "Shutdown may take a while; redis needs to save the entire database";
        echo -n $"Shutting down $prog: "
        /usr/bin/redis-cli shutdown
        if checkpid $PID 2>&1 ; then
            echo_failure
            RETVAL=1
        else
            rm -f /var/lib/redis/temp*rdb
            rm -f /var/lock/subsys/$prog
            echo_success
            RETVAL=0
        fi
    else
        echo -n $"$prog is not running"
        echo_failure
        RETVAL=1
    fi

    echo
    return $RETVAL
}

restart() {
  stop
  start
}

condrestart() {
    [-e /var/lock/subsys/$prog] && restart || :
}

case "$1" in
  start)
  start
  ;;
  stop)
  stop
  ;;
  status)
  status -p %{pid_file} $prog
  RETVAL=$?
  ;;
  restart)
  restart
  ;;
  condrestart|try-restart)
  condrestart
  ;;
   *)
  echo $"Usage: $0 {start|stop|status|restart|condrestart}"
  RETVAL=1
esac

exit $RETVAL
EOF

%build
%{__make}

%install
%{__rm} -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
%{__install} -Dp -m 0755 src/redis-server %{buildroot}%{_sbindir}/redis-server
%{__install} -Dp -m 0755 src/redis-benchmark %{buildroot}%{_bindir}/redis-benchmark
%{__install} -Dp -m 0755 src/redis-cli %{buildroot}%{_bindir}/redis-cli

%{__install} -Dp -m 0755 redis.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/redis
%{__install} -Dp -m 0755 redis.sysv %{buildroot}%{_sysconfdir}/init.d/redis
%{__install} -Dp -m 0644 redis.conf %{buildroot}%{_sysconfdir}/redis.conf

%{__sed} -i 's/daemonize no/daemonize yes/' %{buildroot}%{_sysconfdir}/redis.conf
%{__sed} -i 's/pidfile \/var\/run\/redis.pid/pidfile \/var\/run\/redis\/redis.pid/g' %{buildroot}%{_sysconfdir}/redis.conf
%{__sed} -i 's/dir .\//dir \/var\/lib\/redis\//' %{buildroot}%{_sysconfdir}/redis.conf
%{__sed} -i 's/logfile stdout/logfile \/var\/log\/redis\/redis.log/' %{buildroot}%{_sysconfdir}/redis.conf

%{__install} -p -d -m 0755 %{buildroot}%{_localstatedir}/lib/redis
%{__install} -p -d -m 0755 %{buildroot}%{_localstatedir}/log/redis
%{__install} -p -d -m 0755 %{buildroot}%{_localstatedir}/redis
%{__install} -p -d -m 0755 %{buildroot}%{pid_dir}

%{__install} -p -d -m 0755 %{buildroot}%{_defaultdocdir}/redis-%{version}
%{__install} -Dp -m 0644 00-RELEASENOTES %{buildroot}%{_defaultdocdir}/redis-%{version}/
%{__install} -Dp -m 0644 BUGS %{buildroot}%{_defaultdocdir}/redis-%{version}/
%{__install} -Dp -m 0644 CONTRIBUTING %{buildroot}%{_defaultdocdir}/redis-%{version}/
%{__install} -Dp -m 0644 COPYING %{buildroot}%{_defaultdocdir}/redis-%{version}/
%{__install} -Dp -m 0644 INSTALL %{buildroot}%{_defaultdocdir}/redis-%{version}/
%{__install} -Dp -m 0644 MANIFESTO %{buildroot}%{_defaultdocdir}/redis-%{version}/
%{__install} -Dp -m 0644 README %{buildroot}%{_defaultdocdir}/redis-%{version}/

%pre
/usr/sbin/useradd -c 'User for Redis key-value store' -u 5001 -s /bin/false -r -d %{_localstatedir}/lib/redis redis 2> /dev/null || :

%preun
if [ $1 = 0 ]; then
    # make sure redis service is not running before uninstalling

    # when the preun section is run, we've got stdin attached.  If we
    # call stop() in the redis init script, it will pass stdin along to
    # the redis-cli script; this will cause redis-cli to read an extraneous
    # argument, and the redis-cli shutdown will fail due to the wrong number
    # of arguments.  So we do this little bit of magic to reconnect stdin
    # to the terminal
    term="/dev/$(ps -p$$ --no-heading | awk '{print $2}')"
    exec < $term

    /sbin/service redis stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del redis
fi

%post
/sbin/chkconfig --add redis

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%{_sbindir}/redis-server
%{_bindir}/redis-benchmark
%{_bindir}/redis-cli
%{_sysconfdir}/init.d/redis
%config(noreplace) %{_sysconfdir}/redis.conf
%{_sysconfdir}/logrotate.d/redis
%dir %attr(0770,redis,redis) %{_localstatedir}/lib/redis
%dir %attr(0770,redis,redis) %{_localstatedir}/run/redis
%dir %attr(0770,redis,redis) %{_localstatedir}/log/redis
%dir %attr(0770,redis,redis) %{pid_dir}
%doc %{_defaultdocdir}/redis-%{version}/*

%changelog
* Fri Nov 23 2013 - Robin Kearney <robin@kearney.co.uk>
- Made some minor changes to work with 2.6.4

* Thu Sep 07 2011 - William Gregorian
- pid file path modified to /var/run/redis/
- modified redis.conf vm-max-memory to 1
- modified redis.conf commented out sharedobjects
- modified redis.conf pointed the logs to /var/log/redis/redis.log
