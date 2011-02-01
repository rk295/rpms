#!/bin/bash

cd $1
rpmbuild --define="dist $2" --define="_topdir `pwd`"  -bb SPECS/$1.spec
