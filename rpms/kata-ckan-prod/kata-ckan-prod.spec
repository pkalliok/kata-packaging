# TODO: following comment is partially obsolete/incorrect. See
# autobuild/README for further sudo info
#
# Note: spec file contains calls to sudo. Will not work if not run
# from a terminal or the user executing is not in sudoers appropriately
# This is of course a HACK, but it's caused by the fact the we work
# with a user specific pyenv instead of a system wide installation. 
#
Summary: Kata CKAN production
Name: kata-ckan-prod
%define autov %(echo $AUTOV)
# we had some check here to abort if AUTOV is not set, but it did not
# work. See git history of dev.spec for details
Version: %autov
Release: 1%{?dist}
Group: Applications/File (to be verified)
License: AGPLv3+
#Url: http://not.sure.yet
Source: kata-ckan-prod-%{version}.tgz
Requires: apache-solr
Requires: catdoc
Requires: libxslt
Requires: mcfg
Requires: mod_wsgi
Requires: mod_ssl
Requires: odt2txt
Requires: patch
Requires: policycoreutils-python
Requires: postgresql
Requires: postgresql-server
Requires: rabbitmq-server
Requires: shibboleth
Requires: supervisor
Requires: w3m
Conflicts: kata-ckan-dev
BuildRequires: kata-ckan-dev
# Fedora documentation says one should use...
#BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# but the old-style(?) default %{_topdir}/BUILDROOT/... seems to work nicely
# so we don't clutter yet another place in the directory tree

%define ckanuser ckan
%define scriptdir %{_datadir}/%{name}/setup-scripts
%define patchdir %{_datadir}/%{name}/setup-patches
%define katadocdir %{_datadir}/doc/%{name}

%description
Installs a complete Kata CKAN environment
This package is for the production server.

%prep
%setup


%build
diff -u patches/orig/attribute-map.xml patches/kata/attribute-map.xml >attribute-map.xml.patch || true
diff -u patches/orig/attribute-policy.xml patches/kata/attribute-policy.xml >attribute-policy.xml.patch || true
diff -u patches/orig/httpd.conf patches/kata/httpd.conf >httpd.conf.patch || true
diff -u patches/orig/pg_hba.conf patches/kata/pg_hba.conf >pg_hba.conf.patch || true
diff -u patches/orig/postgresql.conf patches/kata/postgresql.conf >postgresql.conf.patch || true
diff -u patches/orig/shib.conf patches/kata/shib.conf >shib.conf.patch || true
diff -u patches/orig/shibboleth2.xml patches/kata/shibboleth2.xml >shibboleth2.xml.patch || true
diff -u patches/orig/solr.xml patches/kata/solr.xml >solr.xml.patch || true
diff -u patches/orig/ssl.conf patches/kata/ssl.conf >ssl.conf.patch || true
diff -u patches/orig/tomcat6.conf patches/kata/tomcat6.conf >tomcat6.conf.patch || true


%install
# cpio: we need to be root to be able to read, but we don't preserve the 
# ownership because rpmbuild will in trouble later with such files. 
# %attr will take care of ownership eventually
# sudo is somewhat nasty here (interactive command) but building is
# only carried out by people who know what they are doing...
me=$(whoami)
# run a dummy sudo first. Two sudo commands in a pipe sometimes screw up
# the terminal when both prompting for the password
sudo true
sudo find /home/%{ckanuser}/pyenv -depth | sudo cpio -pdm --owner ${me}: $RPM_BUILD_ROOT/
# not sure why, but testings show that the following 2 directories are not
# owned by ${me}
sudo chown ${me} $RPM_BUILD_ROOT/home
sudo chown ${me} $RPM_BUILD_ROOT/home/%{ckanuser}
find $RPM_BUILD_ROOT/home/%{ckanuser} -name .git -print0 | xargs -0 rm -rf
find $RPM_BUILD_ROOT/home/%{ckanuser} -name .gitignore -print0 | xargs -0 rm -f
find $RPM_BUILD_ROOT/home/%{ckanuser} -name .svn -print0 | xargs -0 rm -rf
find $RPM_BUILD_ROOT/home/%{ckanuser} -name .bzr -print0 | xargs -0 rm -rf
find $RPM_BUILD_ROOT/home/%{ckanuser} -name .bzrignore -print0 | xargs -0 rm -f

# Remove the symlink to orange and actually copy the file over
rm $RPM_BUILD_ROOT/home/%{ckanuser}/pyenv/lib/python2.6/site-packages/Orange/liborange.so
cp $RPM_BUILD_ROOT/home/%{ckanuser}/pyenv/lib/python2.6/site-packages/Orange/orange.so $RPM_BUILD_ROOT/home/%{ckanuser}/pyenv/lib/python2.6/site-packages/Orange/liborange.so

install -d $RPM_BUILD_ROOT/%{scriptdir}
install -d $RPM_BUILD_ROOT/%{patchdir}
install -d $RPM_BUILD_ROOT/%{katadocdir}
# following directories owned by other packages, but we need them in the
# build root
install -d $RPM_BUILD_ROOT/etc/cron.daily
install -d $RPM_BUILD_ROOT/etc/cron.hourly
install -d $RPM_BUILD_ROOT/etc/httpd/conf.d
install -d $RPM_BUILD_ROOT/etc/sysconfig/pgsql

# setup scripts (keep them numerically ordered)
install 04configuredependencies.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 16configshibbolethsp.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 20setuppostgres.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 22configsolr.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 24setupapachessl.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 32setupckan-root.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 36initckandb.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 40setupapache.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 48initextensionsdb.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 61setupsources.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 80backuphome.sh $RPM_BUILD_ROOT/%{scriptdir}/
# misc scripts (keep them alphabetically ordered by filename)
install runharvester.sh $RPM_BUILD_ROOT/%{scriptdir}/
# patches (keep them alphabetically ordered by filename)
install attribute-map.xml.patch $RPM_BUILD_ROOT/%{patchdir}/
install attribute-policy.xml.patch $RPM_BUILD_ROOT/%{patchdir}/
install httpd.conf.patch $RPM_BUILD_ROOT/%{patchdir}/
install pg_hba.conf.patch $RPM_BUILD_ROOT/%{patchdir}/
install postgresql.conf.patch $RPM_BUILD_ROOT/%{patchdir}/
install shib.conf.patch $RPM_BUILD_ROOT/%{patchdir}/
install shibboleth2.xml.patch $RPM_BUILD_ROOT/%{patchdir}/
install solr.xml.patch $RPM_BUILD_ROOT/%{patchdir}/
install ssl.conf.patch $RPM_BUILD_ROOT/%{patchdir}/
install tomcat6.conf.patch $RPM_BUILD_ROOT/%{patchdir}/

# misc data/conf files (keep them alphabetically ordered by filename)
install kataemail $RPM_BUILD_ROOT/etc/cron.daily/
install kataharvesterjobs $RPM_BUILD_ROOT/etc/cron.daily/
install kataindex $RPM_BUILD_ROOT/etc/cron.hourly/
install katatracking $RPM_BUILD_ROOT/etc/cron.daily/
install harvester.conf $RPM_BUILD_ROOT/%{scriptdir}/
install kata.conf $RPM_BUILD_ROOT/etc/httpd/conf.d/
install postgresql $RPM_BUILD_ROOT/etc/sysconfig/pgsql/

# documentation (version info)
install /usr/share/kata-ckan-dev/setup-data/pip.freeze.current $RPM_BUILD_ROOT/%{katadocdir}/

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%attr(-,%{ckanuser},%{ckanuser}) /home/%{ckanuser}/pyenv
%{scriptdir}/04configuredependencies.sh
%{scriptdir}/16configshibbolethsp.sh
%{scriptdir}/20setuppostgres.sh
%{scriptdir}/22configsolr.sh
%{scriptdir}/24setupapachessl.sh
%{scriptdir}/32setupckan-root.sh
%{scriptdir}/36initckandb.sh
%{scriptdir}/40setupapache.sh
%{scriptdir}/48initextensionsdb.sh
%{scriptdir}/61setupsources.sh
%{scriptdir}/80backuphome.sh
%{scriptdir}/runharvester.sh
%{patchdir}/httpd.conf.patch
%{patchdir}/pg_hba.conf.patch
%{patchdir}/postgresql.conf.patch
%attr(0655,root,root)/etc/cron.hourly/kataindex
%attr(0655,root,root)/etc/cron.daily/kataemail
%attr(0655,root,root)/etc/cron.daily/kataharvesterjobs
%attr(0655,root,root)/etc/cron.daily/katatracking
%{scriptdir}/harvester.conf
/etc/httpd/conf.d/kata.conf
/etc/sysconfig/pgsql/postgresql

%{patchdir}/attribute-map.xml.patch
%{patchdir}/attribute-policy.xml.patch
%{patchdir}/shib.conf.patch
%{patchdir}/shibboleth2.xml.patch
%{patchdir}/solr.xml.patch
%{patchdir}/ssl.conf.patch
%{patchdir}/tomcat6.conf.patch

# documentation (version info)
%{katadocdir}/pip.freeze.current

%pre
useradd %{ckanuser}  # needs to be removed if ckanuser were changed to httpd

%post
%{scriptdir}/04configuredependencies.sh %{patchdir}
%{scriptdir}/16configshibbolethsp.sh "/usr/share/kata-ckan-prod"
%{scriptdir}/20setuppostgres.sh %{patchdir}
%{scriptdir}/22configsolr.sh /home/%{ckanuser} %{patchdir}
%{scriptdir}/24setupapachessl.sh "/usr/share/kata-ckan-prod"
%{scriptdir}/32setupckan-root.sh %{ckanuser}
su -c "%{scriptdir}/36initckandb.sh /home/%{ckanuser}" %{ckanuser}
%{scriptdir}/40setupapache.sh %{patchdir}
su -c "%{scriptdir}/48initextensionsdb.sh /home/%{ckanuser}" %{ckanuser}

# Lets do this last so our harvesters are correctly picked up by the daemons.
cat /usr/share/kata-ckan-prod/setup-scripts/harvester.conf >> /etc/supervisord.conf
# Enable tmp directory for logging. Otherwise goes to /
sed -i 's/;directory/directory/' /etc/supervisord.conf
chkconfig supervisord on
%{scriptdir}/61setupsources.sh /home/%{ckanuser}
service atd restart
at -f %{scriptdir}/runharvester.sh 'now + 3 minute'

service shibd start
service httpd start
service supervisord start
service crond start


%preun
# design assumption is that kata is on a "single purpose" server, we 
# initialize services like postgres during installation, so we also stop 
# them here
service supervisord stop
service rabbitmq-server stop
service httpd stop
service shibd stop
service tomcat6 stop
service postgresql stop

%postun
userdel -r %{ckanuser}


%changelog
* Thu Dec 13 2012 Uwe Geuder <uwe.geuder@nomovok.com>
  Changelog not maintained here, see git(hub) for full history

* Tue Sep 11 2012 Harri Palojärvi <harri.palojarvi@nomovok.com>
- Added shibboleth

* Mon May 22 2012 Uwe Geuder <uwe.geuder@nomovok.com>
- Initial version
