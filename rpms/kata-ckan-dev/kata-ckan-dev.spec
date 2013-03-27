Summary: Development and packaging environment for Kata CKAN
Name: kata-ckan-dev
%define autov %(echo $AUTOV)
# we had some check here to abort if AUTOV is not set, but it did not
# work. See git history for details
Version: %autov
Release: 1%{?dist}
Group: Applications/File (to be verified)
License: AGPLv3+
#Url: http://not.sure.yet
Source0: kata-ckan-dev-%{version}.tgz
Requires: apache-solr
Requires: bzr
Requires: catdoc
Requires: gcc
Requires: gcc-c++
Requires: git
Requires: libxslt-devel
Requires: mcfg
Requires: mod_ssl
Requires: mod_wsgi
Requires: numpy
Requires: odt2txt
Requires: patch
Requires: policycoreutils-python
Requires: postgresql-devel
Requires: postgresql-server
Requires: python-devel
Requires: rabbitmq-server
Requires: shibboleth
Requires: supervisor
Requires: w3m
Conflicts: kata-ckan-prod
# Fedora documentation says one should use...
#BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# but the old-style(?) default %{_topdir}/BUILDROOT/... seems to work nicely
# so we don't clutter yet another place in the directory tree

%define ckanuser ckan
%define scriptdir %{_datadir}/%{name}/setup-scripts
%define patchdir %{_datadir}/%{name}/setup-patches
%define katadatadir %{_datadir}/%{name}/setup-data

%description
Installs a CKAN environment using pip.
This package is for internal development use only. Not intended to be used
on production systems. After installing a development system build
a kata-ckan-prod.rpm package to capture the result of this installation.


%prep
%setup

%build
# keep patches ordered alphabetically
diff -u patches/orig/attribute-map.xml patches/kata/attribute-map.xml >attribute-map.xml.patch || true
diff -u patches/orig/attribute-policy.xml patches/kata/attribute-policy.xml >attribute-policy.xml.patch || true
diff -u patches/orig/development.ini patches/kata/development.ini >development.ini.patch || true
diff -u patches/orig/httpd.conf patches/kata/httpd.conf >httpd.conf.patch || true
diff -u patches/orig/pg_hba.conf patches/kata/pg_hba.conf >pg_hba.conf.patch || true
diff -u patches/orig/postgresql.conf patches/kata/postgresql.conf >postgresql.conf.patch || true
diff -u patches/orig/shib.conf patches/kata/shib.conf >shib.conf.patch || true
diff -u patches/orig/shibboleth2.xml patches/kata/shibboleth2.xml >shibboleth2.xml.patch || true
diff -u patches/orig/solr.xml patches/kata/solr.xml >solr.xml.patch || true
diff -u patches/orig/ssl.conf patches/kata/ssl.conf >ssl.conf.patch || true
diff -u patches/orig/tomcat6.conf patches/kata/tomcat6.conf >tomcat6.conf.patch || true
diff -u patches/orig/who.ini patches/kata/who.ini >who.ini.patch || true

%install
install -d $RPM_BUILD_ROOT/%{scriptdir}
install -d $RPM_BUILD_ROOT/%{patchdir}
install -d $RPM_BUILD_ROOT/%{katadatadir}
# following directories owned by other packages, but we need them in the
# build root
install -d $RPM_BUILD_ROOT/etc/cron.daily
install -d $RPM_BUILD_ROOT/etc/cron.hourly
install -d $RPM_BUILD_ROOT/etc/httpd/conf.d
install -d $RPM_BUILD_ROOT/etc/sysconfig/pgsql

# setup scripts (keep them numerically ordered)
install 04configuredependencies.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 08getpyenv.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 12getpythonpackages.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 16configshibbolethsp.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 20setuppostgres.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 22configsolr.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 24setupapachessl.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 28setupckan.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 32setupckan-root.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 36initckandb.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 40setupapache.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 44installckanextensions.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 48initextensionsdb.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 61setupsources.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 70checkpythonpackages.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 71storepythonpackages.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 80backuphome.sh $RPM_BUILD_ROOT/%{scriptdir}/

# misc scripts (keep them alphabetically ordered by filename)
install runharvester.sh $RPM_BUILD_ROOT/%{katadatadir}/

# patches (keep them alphabetically ordered by filename)
install attribute-map.xml.patch $RPM_BUILD_ROOT/%{patchdir}/
install attribute-policy.xml.patch $RPM_BUILD_ROOT/%{patchdir}/
install development.ini.patch $RPM_BUILD_ROOT/%{patchdir}/
install httpd.conf.patch $RPM_BUILD_ROOT/%{patchdir}/
install pg_hba.conf.patch $RPM_BUILD_ROOT/%{patchdir}/
install postgresql.conf.patch $RPM_BUILD_ROOT/%{patchdir}/
install shib.conf.patch $RPM_BUILD_ROOT/%{patchdir}/
install shibboleth2.xml.patch $RPM_BUILD_ROOT/%{patchdir}/
install solr.xml.patch $RPM_BUILD_ROOT/%{patchdir}/
install ssl.conf.patch $RPM_BUILD_ROOT/%{patchdir}/
install tomcat6.conf.patch $RPM_BUILD_ROOT/%{patchdir}/
install who.ini.patch $RPM_BUILD_ROOT/%{patchdir}/

# misc data/conf files (keep them alphabetically ordered by filename)
install kataemail $RPM_BUILD_ROOT/etc/cron.daily/
install kataharvesterjobs $RPM_BUILD_ROOT/etc/cron.daily/
install kataindex $RPM_BUILD_ROOT/etc/cron.hourly/
install katatracking $RPM_BUILD_ROOT/etc/cron.daily/
install harvester.conf $RPM_BUILD_ROOT/%{katadatadir}/
install kata.conf $RPM_BUILD_ROOT/etc/httpd/conf.d/
install log/pip.freeze.lastknown $RPM_BUILD_ROOT/%{katadatadir}/
install postgresql $RPM_BUILD_ROOT/etc/sysconfig/pgsql/

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
# same order as above
%{scriptdir}/04configuredependencies.sh
%{scriptdir}/08getpyenv.sh
%{scriptdir}/12getpythonpackages.sh
%{scriptdir}/16configshibbolethsp.sh
%{scriptdir}/20setuppostgres.sh
%{scriptdir}/22configsolr.sh
%{scriptdir}/24setupapachessl.sh
%{scriptdir}/28setupckan.sh
%{scriptdir}/32setupckan-root.sh
%{scriptdir}/36initckandb.sh
%{scriptdir}/40setupapache.sh
%{scriptdir}/44installckanextensions.sh
%{scriptdir}/48initextensionsdb.sh
%{scriptdir}/61setupsources.sh
%{scriptdir}/70checkpythonpackages.sh
%{scriptdir}/71storepythonpackages.sh
%{scriptdir}/80backuphome.sh

# sic! following script in datadir
%{katadatadir}/runharvester.sh
%{patchdir}/attribute-map.xml.patch
%{patchdir}/attribute-policy.xml.patch
%{patchdir}/development.ini.patch
%{patchdir}/httpd.conf.patch
%{patchdir}/pg_hba.conf.patch
%{patchdir}/postgresql.conf.patch
%{patchdir}/shib.conf.patch
%{patchdir}/shibboleth2.xml.patch
%{patchdir}/solr.xml.patch
%{patchdir}/ssl.conf.patch
%{patchdir}/tomcat6.conf.patch
%{patchdir}/who.ini.patch
%attr(0655,root,root)/etc/cron.daily/kataemail
%attr(0655,root,root)/etc/cron.daily/kataharvesterjobs
%attr(0655,root,root)/etc/cron.hourly/kataindex
%attr(0655,root,root)/etc/cron.daily/katatracking
%{katadatadir}/harvester.conf
/etc/httpd/conf.d/kata.conf
%{katadatadir}/pip.freeze.lastknown
/etc/sysconfig/pgsql/postgresql

%post
useradd %{ckanuser}  # would need to be removed if ckanuser were changed to httpd
%{scriptdir}/04configuredependencies.sh %{patchdir}
su -c "%{scriptdir}/08getpyenv.sh /home/%{ckanuser}" %{ckanuser}
su -c "%{scriptdir}/12getpythonpackages.sh /home/%{ckanuser}" %{ckanuser}
%{scriptdir}/16configshibbolethsp.sh "/usr/share/kata-ckan-dev"
%{scriptdir}/20setuppostgres.sh %{patchdir}
%{scriptdir}/22configsolr.sh /home/%{ckanuser} %{patchdir}
%{scriptdir}/24setupapachessl.sh "/usr/share/kata-ckan-dev"
cat > /home/%{ckanuser}/pyenv/bin/wsgi.py <<EOF
import os
instance_dir = '/home/ckan'
config_file = '/etc/kata.ini'
pyenv_bin_dir = os.path.join(instance_dir, 'pyenv', 'bin')
activate_this = os.path.join(pyenv_bin_dir, 'activate_this.py')
execfile(activate_this, dict(__file__=activate_this))
from paste.deploy import loadapp
config_filepath = os.path.join(instance_dir, config_file)
from paste.script.util.logging_config import fileConfig
fileConfig(config_filepath)
application = loadapp('config:%s' % config_filepath)
EOF
chmod 777 /home/%{ckanuser}/pyenv/bin/wsgi.py
su -c "%{scriptdir}/28setupckan.sh /home/%{ckanuser}" %{ckanuser}
%{scriptdir}/32setupckan-root.sh %{ckanuser}
su -c "%{scriptdir}/36initckandb.sh /home/%{ckanuser}" %{ckanuser}
%{scriptdir}/40setupapache.sh %{patchdir}
su -c "%{scriptdir}/44installckanextensions.sh /home/%{ckanuser}" %{ckanuser}
# no need to call 48initextensionsdb.sh here, previous script does it because
# it needs in in the middle
# Let's configure supervisor now, so our harvesters are correctly picked up by
# the daemons.
cat /usr/share/kata-ckan-dev/setup-data/harvester.conf >> /etc/supervisord.conf
# Enable tmp directory for logging. Otherwise goes to /
sed -i 's/;directory/directory/' /etc/supervisord.conf
%{scriptdir}/61setupsources.sh /home/%{ckanuser}
service atd restart
at -f %{katadatadir}/runharvester.sh 'now + 3 minute'

service shibd start
service httpd start
service supervisord start
service crond start
# run this last so the user has a chance to see the output
su -c "%{scriptdir}/70checkpythonpackages.sh /home/%{ckanuser} %{katadatadir}/pip.freeze.lastknown" %{ckanuser}
# well, actually it was last but one, but we still need to do this as root
# afterwards
%{scriptdir}/71storepythonpackages.sh %{katadatadir}

%preun
service ckan-dev stop
%{scriptdir}/80backuphome.sh /home/%{ckanuser}


%postun
echo "Uninstallation not fully supported yet, better get a clean VM to be sure"
echo "User account %{ckanuser} not deleted, firewall change not reverted,"
echo "postgresql configuration not reverted"

%changelog
* Mon May 21 2012 Uwe Geuder <uwe.geuder@nomovok.com>
- Initial version
