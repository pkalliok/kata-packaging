#! /bin/sh
# configure our dependencies (packages which have been installed before)
set -x
if [ -f /tmp/kata-SKIP04 ]
then
  echo "Skipping 04"
  exit 0
fi
patchdir=$1

# the rpm package has installed several jobs to cron.daily
# because ckan is not yet readily installed they will fail if run now
# stop crond here to avoid this (actually there is a small window
# of opportunity that it has already happened. It's not really fatal,
# but a nuisance because
# a.) root will receive unecessary mail.
# b.) We miss real problems with the cron jobs because they won't be rerun
#     until the next day
# This typically happened in dev.rpm installation, because dev installation
# lasts 55-58 minutes
#
# anacron, which is executing the /etc/cron.daily jobs might already be
# running and waiting for one of its delays. Stop it, too.
# It will be started by cron the next hour, find its timestamps not updated
# and do the work. No need for us to restart it.
#
# pkill has no verbose option, but should there be the need to debug yet
# another problmem /var/log/cron will contain the information
# wether it had a victim
#
# stop anacron first because that's the critical time window
pkill -USR1 anacron
service crond stop
# anacron once more just in case crond managed to start it in this very
# subsecond ...
pkill -USR1 anacron

service tomcat6 stop
cd /etc/tomcat6
patch -b -p2 -i "${patchdir}/tomcat6.conf.patch"
python /usr/share/mcfg/tool/mcfg.py run /usr/share/mcfg/config/kata-template.ini /root/kata-master.ini 4
service tomcat6 start
# only apache account has access to the DB (besides postgres admin), allow it
# to run setup scripts and cron jobs
chsh -s /bin/bash apache
# the following mkdir will fail in prod.rpm because the directory already 
# exists when this script is executed
# no need to add any logic, the failure does not harm
mkdir /home/ckan
chown apache:apache /home/ckan
