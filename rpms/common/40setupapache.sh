#! /bin/sh
set -x
if [ -f /tmp/kata-SKIP40 ]
then
  echo "Skipping 40"
  exit 0
fi
patchdir="$1"
service httpd stop
pushd /etc/httpd/conf >/dev/null
patch -b -p2 -i ${patchdir}/httpd.conf.patch
python /usr/share/mcfg/tool/mcfg.py run /usr/share/mcfg/config/kata-template.ini /root/kata-master.ini 40
popd >/dev/null
chkconfig httpd on
chown -R ckan:apache /home/ckan/pyenv
chmod -R 755 /home/ckan
setsebool -P httpd_can_network_connect 1
# TODO: chcon is not the right thing here. Everything will break when
# restorecon is run. See 20setuppostgres.sh for the correct solution
chcon -R --type=httpd_sys_content_t /home/ckan
touch /home/ckan/pyenv/ckan.log
chown ckan:apache /home/ckan/pyenv/ckan.log
chmod g+w /home/ckan/pyenv/ckan.log
chown -R ckan:apache /opt/data/ckan
chcon -R --type=httpd_sys_content_t /opt/data/ckan
chmod -R g+w /opt/data/ckan/{data,sstore,data_tree}
mkdir /var/www/.orange
chown apache:apache /var/www/.orange
# TODO: We should not hack other packages' files
# what will happen when Python gets a security update???
# well, as long as we do it only in dev it doesn't matter, because
# dev systems does not live very long
for dir in $(echo /usr/lib*/python2.6)
# loop exists to handle both 32 and 64 bit installations. Not sure whether
# it could ever be run more than once, but that doesn't matter 
do
  sed -i.orig 's/CFUNCTYPE(c_int)(lambda: None)/#CFUNCTYPE(c_int)(lambda: None)/' ${dir}/ctypes/__init__.py
done
