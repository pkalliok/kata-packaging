#! /bin/sh
set -x
if [ -f /tmp/kata-SKIP20 ]
then
  echo "Skipping 20"
  exit 0
fi
patchdir="$1"
# postgresql-server rpm creates 2 directories under the default location:
# data and backups
# let's do the same under our custom location
if [ \! -e /opt/data/pgsql ]
then
  # try to build the same hierarchy as postgresql-server.rpm did it for
  # the default location
  mkdir -p /opt/data/pgsql/data
  mkdir /opt/data/pgsql/backups
  chown -R postgres:postgres /opt/data/pgsql
  chmod -R og= /opt/data/pgsql
  # chcon is not enough. service postgresql runs restorecon
  # the exact rules are a bit guessing, especially for the
  # backups directory
  # well, we could save at least one or two restorecon commands here,
  # because they are repeated soon, but they are quick and it's easier
  # to debug what happens here
  semanage fcontext -a -t var_lib_t /opt/data/pgsql
  restorecon /opt/data/pgsql
  semanage fcontext -a -t postgresql_db_t "/opt/data/pgsql/data(/.*)?"
  restorecon /opt/data/pgsql/data
  semanage fcontext -a -t var_lib_t "/opt/data/pgsql/backups(/.*)?"
  restorecon /opt/data/pgsql/backups
  # the following seems to be necessary to work around a bug(?) in 
  # postgres setup
  # normally initdb takes care of this, but if the DB directory has been
  # changed to a non-standard location it does not work. The DB still works
  # but pgstartup.log will never be written. Better to have the log just in case
  # something goes wrong
  touch /opt/data/pgsql/pgstartup.log
  chown postgres:postgres /opt/data/pgsql/pgstartup.log
  semanage fcontext -a -t postgresql_db_t /opt/data/pgsql/pgstartup.log
  restorecon /opt/data/pgsql/pgstartup.log
fi
pushd /opt/data/pgsql/data >/dev/null
datafiles=$(ls | wc -l)
if [ $datafiles -ne 0 ]
then
  # assume that if there is any DB configuration, it is a valid CKAN DB
  # this is of course not really true
  echo "some database configuration found, don't overwrite it"
  touch /tmp/kata-SKIP-dbinit
  service postgresql start
else
  rm -f /tmp/kata-SKIP-dbinit 2>/dev/null
  service postgresql initdb
  # su postgres ensures that the resulting file has the correct owner
  su -c "patch -b -p2 -i ${patchdir}/pg_hba.conf.patch" postgres
  su -c "patch -b -p2 -i ${patchdir}/postgresql.conf.patch" postgres
  cp /root/kata-master.ini /opt/data/pgsql
  su -c "python /usr/share/mcfg/tool/mcfg.py switchuser root postgres" postgres
  su -c "python /usr/share/mcfg/tool/mcfg.py run /usr/share/mcfg/config/kata-template.ini /opt/data/pgsql/kata-master.ini 20" postgres
  python /usr/share/mcfg/tool/mcfg.py switchuser postgres root
  rm /opt/data/pgsql/kata-master.ini
  # mcfg should really preserve the file mode, but as it doesn't we fix it here
  chmod og-r /opt/data/pgsql/data/postgresql.conf

  popd >/dev/null
  service postgresql start
  chkconfig postgresql on
  sleep 3    # creating the user happened to fail sometimes, wait a moment
  su -c "createuser -S -D -R apache" postgres
  su -c "createdb -O apache ckandb" postgres
fi
