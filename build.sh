#!/bin/bash

cd $1
rpmbuild --define="dist $2" --define="_topdir `pwd`"  -bb SPECS/$1.spec
rpmbuild --define="dist $2" --define="_topdir `pwd`"  -bs SPECS/$1.spec
rm -rf BUILD/*
