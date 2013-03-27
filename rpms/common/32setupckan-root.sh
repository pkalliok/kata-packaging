#! /bin/sh
# this script is run as root (previous NNsetupckan.sh as %ckanuser)
set -x
if [ -f /tmp/kata-SKIP32 ]
then
  echo "Skipping 32"
  exit 0
fi
ckauser=$1
mkdir -p /opt/data/ckan
pushd /opt/data/ckan >/dev/null
mkdir data sstore data_tree
chown ${ckauser}:${ckanuser} data sstore data_tree
# Apache setup script will later change this again, but let's simulate the
# previous behavior when these directories where still in the pyenv code
# tree and created by ckanuser

mkdir /var/log/ckan   # development.ini says this directory is used for
                      # script output. don't think we have seen any yet
                      # not sure what protections should be

cp /home/ckan/pyenv/src/ckan/development.ini /etc/kata.ini
python /usr/share/mcfg/tool/mcfg.py run /usr/share/mcfg/config/kata-template.ini /root/kata-master.ini 31
# run it a second time to support replace_by_ip for development systems
# previous increment number "stolen" from non-existing script 31...
python /usr/share/mcfg/tool/mcfg.py run /usr/share/mcfg/config/kata-template.ini /root/kata-master.ini 32
# set same rights as development.ini used to have (from 32setupapache.sh)
# this also allows 36ckaninstallenxtensions.sh to edit the extensions list
chown  ckan:apache /etc/kata.ini
chmod -R 755 /home/ckan
semanage fcontext -a -t httpd_sys_content_t /etc/kata.ini
restorecon /etc/kata.ini
