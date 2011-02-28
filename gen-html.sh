#!/bin/bash
UrlBase="http://svn.riviera.org.uk/repo/RPMS"

StarDir=`pwd`

echo "<ul>"
for Package in * ; do 

	if [ -d $Package ] ; then
		cd $Package
		echo "<lh>$Package</li><ul>"
		for RPM in `find . -name \*.rpm` ; do
			
			tmp=$(echo $RPM | sed 's/^\.//g')
			RPM=$tmp
			
			FileName=$(basename $RPM)
			echo "<li><a href=\"${UrlBase}/${Package}${RPM}\">$FileName</a>"
		done
		echo "</ul>"
	fi


	cd $StarDir
done
echo "</ul>"
