#!/bin/sh
set -x
if [ -f /tmp/kata-SKIP22 ]
then
  echo "Skipping 22"
  exit 0
fi
instloc=$1
patchdir=$2

service tomcat6 stop
pushd /opt/data/solr/ >/dev/null
patch -b -p2 -i "${patchdir}/solr.xml.patch"
popd >/dev/null

cd /etc/tomcat6
patch -b -p2 -i "${patchdir}/tomcat6.conf.patch"

/usr/bin/python /usr/share/mcfg/tool/mcfg.py run /usr/share/mcfg/config/kata-template.ini /root/kata-master.ini 22

postfix=-$(date +%y%m%d-%H%M%S)
cp /opt/data/solr/collection1/conf/schema.xml /opt/data/solr/collection1/conf/schema.xml.bak-${postfix}
cp $instloc/pyenv/src/ckan/ckan/config/solr/schema-2.0.xml /opt/data/solr/collection1/conf/schema.xml
chown tomcat:tomcat /opt/data/solr/solr.xml
service tomcat6 start

chkconfig tomcat6 on
