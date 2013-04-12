#!/bin/sh
set -x
if [ -f /tmp/kata-SKIP61 ]
then
  echo "Skipping 61"
  exit 0
fi
instloc=$1
ckanuser=$2
service rabbitmq-server start
chkconfig rabbitmq-server on
if [ \! -e /tmp/kata-SKIP-dbinit ]
then
  su ${ckanuser} <<EOF
  $instloc/pyenv/bin/paster --plugin=ckanext-harvest harvester source file:///home/ckan/pyenv/src/ckanext-ddi/ddi3.txt DDI3 --config=/etc/kata.ini
  $instloc/pyenv/bin/paster --plugin=ckanext-harvest harvester source http://www.fsd.uta.fi/fi/aineistot/luettelo/fsd-ddi-records-uris-fi.txt DDI --config=/etc/kata.ini
  $instloc/pyenv/bin/paster --plugin=ckanext-harvest harvester source http://helda.helsinki.fi/oai/request OAI-PMH --config=/etc/kata.ini
EOF
fi
chkconfig supervisord on
# according to an earlier comment supervisor cannot be started before
# apache is (re)started. Because apache is nowadays started at the end
# of the installation, also starting supvisord happens there
