#! /bin/sh
# remember: we are not root here (%ckanuser from the spec file)
set -x
if [ -f /tmp/kata-SKIP48 ]
then
  echo "Skipping 48"
  exit 0
fi
instloc=$1
cd $instloc
if [ \! -e /tmp/kata-SKIP-dbinit ]
then
  source pyenv/bin/activate
  paster --plugin=ckanext-harvest harvester initdb --config=/etc/kata.ini
  paster --plugin=ckanext-kata katacmd initdb --config=/etc/kata.ini
else
  # CKAN DB exists, no need to init harvester DB either
  true
fi 
