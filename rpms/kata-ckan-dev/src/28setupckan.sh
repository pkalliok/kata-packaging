#! /bin/sh
# remember: we are not root here (%ckanuser from the spec file)
set -x
if [ -f /tmp/kata-SKIP28 ]
then
  echo "Skipping 28"
  exit 0
fi
instloc=$1
cd $instloc
source pyenv/bin/activate
cd pyenv/src/ckan
paster make-config ckan development.ini

# if generated random stuff is too close to lines we need to patch
# patch command will complain and eventually reject hunks
#
# extract generated random stuff before patching and re-insert it after
# patching
# keep intermediate in /tmp just in case we need to debug. This is the
# development machine, no need to clean up
cp development.ini development.ini.generated-orig
grep -e ^beaker\.session.\secret -e ^app_instance_uuid development.ini >/tmp/development.ini.generated-only
sed -i -e "/^beaker\.session\.secret/ d" -e s/^app_instance_uuid.*/%%GENERATED%%/ development.ini
patch -b -p2 -i /usr/share/kata-ckan-dev/setup-patches/development.ini.patch
mv development.ini development.ini.patched
sed -e "/%%GENERATED%%/ r /tmp/development.ini.generated-only" -e "/%%GENERATED%%/ d" development.ini.patched > development.ini
# patching done...
