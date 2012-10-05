#!/bin/sh
set -x
instloc=$1
extensions="shibboleth harvest oaipmh_harvester synchronous_search oaipmh ddi_harvester sitemap"
kata_extensions=" kata kata_metadata"
sed -i "/^ckan.plugins/s|$| $extensions|" $instloc/pyenv/src/ckan/development.ini
sed -i "/^ckan.plugins/s|$| $kata_extensions|" $instloc/pyenv/src/ckan/development.ini
sed -i "/^ckan.plugins/s|$| $extensions|" $instloc/pyenv/src/ckan/harvester.ini
# with the internal development server we used to call...
#
#   service ckan-dev restart
#
# ... here.
# I don't think the equivalent is needed with Apache, because it should 
# not have loaded any Python code yet
