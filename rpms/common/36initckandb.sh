#! /bin/sh
# remember: we are not root here (but apache)
set -x
if [ -f /tmp/kata-SKIP36 ]
then
  echo "Skipping 36"
  exit 0
fi
instloc=$1
cd $instloc
source pyenv/bin/activate
cd pyenv/src/ckan
if [ \! -e /tmp/kata-SKIP-dbinit ]
then
  paster --plugin=ckan db init --config=/etc/kata.ini
else
  paster --plugin=ckan db upgrade --config=/etc/kata.ini
fi
