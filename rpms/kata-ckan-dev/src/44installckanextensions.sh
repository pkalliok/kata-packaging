#!/bin/sh
# remember: we are not root here (%ckanuser from the spec file)
set -x
if [ -f /tmp/kata-SKIP44 ]
then
  echo "Skipping 44"
  exit 0
fi
instloc=$1

cd $instloc/pyenv
source ./bin/activate
cd src/ckan
if [ -r /etc/kata-ckan-dev/versions ]
then
   source /etc/kata-ckan-dev/versions
else
   ext_harvest_version=""
   ext_urn_version=""
   ext_oaipmh_version=""
   ext_ddi_version=""
   ext_sitemap_version=""
   ext_shibboleth_version=""
   ext_kata_version=""
   # well missing assignments would have had the same effect as empty values
   # but let's have them here for clarity. Maybe we want to hard-code
   # some values here in a later project phase
fi

theirurl='git+https://github.com/okfn/ckanext-harvest.git'
oururl='git+https://github.com/kata-csc/ckanext-harvest.git'
pip install -e ${oururl}${ext_harvest_version}#egg=ckanext-harvest
pip install carrot

pip install -e git+https://github.com/kata-csc/ckanext-urn.git${ext_urn_version}#egg=ckanext-urn

pip install -e git+https://github.com/kata-csc/ckanext-oaipmh.git${ext_oaipmh_version}#egg=ckanext-oaipmh

# Install bazaar version of BeautifulSoup, counter the DDI3 bug.
pip install -e bzr+lp:beautifulsoup#egg=BeautifulSoup
pip install -e git+https://github.com/kata-csc/ckanext-ddi.git${ext_ddi_version}#egg=ckanext-ddi

pip install -e git+https://github.com/kata-csc/ckanext-sitemap.git${ext_sitemap_version}#egg=ckanext-sitemap

pip install -e git+git://github.com/kata-csc/ckanext-shibboleth.git${ext_shibboleth_version}#egg=ckanext-shibboleth
patch -b -p2 -i /usr/share/kata-ckan-dev/setup-patches/who.ini.patch

pip install -e git+git://github.com/kata-csc/ckanext-kata.git${ext_kata_version}#egg=ckanext-kata

$(dirname $0)/48initextensionsdb.sh $instloc
# this script is dev only, so no problem with the password on github
paster --plugin=ckan user add harvester password=harvester email=harvester@harvesting.none --config=/etc/kata.ini
paster --plugin=ckan sysadmin add harvester --config=/etc/kata.ini

extensions="shibboleth harvest oaipmh_harvester synchronous_search oaipmh ddi_harvester sitemap kata kata_metadata ddi3_harvester"
# first change in the ini template that will be packaged for prod
cp development.ini development.ini.backup.preext
sed -i "/^ckan.plugins/s|$| $extensions|" development.ini
# second change in the ini file that is used in dev
# cannot sed -i here because we have only write access to the file but not to
# the directory (sed -i creates a tmp file in the same dir)
# (redirection into existing file keeps ownership, protections
# and selinux labeling)
cp /etc/kata.ini /tmp/kata.ini
sed "/^ckan.plugins/s|$| $extensions|" /tmp/kata.ini >/etc/kata.ini
rm /tmp/kata.ini
