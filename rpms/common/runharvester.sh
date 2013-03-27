#!/bin/sh
/home/ckan/pyenv/bin/paster --plugin=ckanext-harvest harvester run --config=/etc/kata.ini > /dev/null 2>&1