RPMS
====

This is a small repo of some RPMs I've built over the years because I couldn't
find suitable ones. Mostly built for Centos/RHEL 5/6 i686 and x86_64.

Each package directory contains the following:

* RPMS
* SOURCES
* SPECS
* SRPMS

Mostly you'll be interested in <package>/RPMS/ but if the binary RPM you want 
isn't in there, feel free to clone the repo and build it. 

There are a couple of helper scripts int he top level directory:

* build.sh - takes two args, name of package and dist - eg el6:
    ./build.sh rinetd el6 will build a RHEL6 package of rinetd. Worth noting
               the el6 string is only used in the package file name for 
               identification.  It does no sanity checking that you are actually
               on RHEL 6!

* mkdirs - creates an empty package directory structure
* gen-html.sh - used to make a quick index to put on my site (http://riviera.org.uk)
