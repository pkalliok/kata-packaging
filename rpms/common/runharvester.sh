#!/bin/sh
su apache <<'EOF'
  /home/ckan/pyenv/bin/paster --plugin=ckanext-harvest harvester run --config=/etc/kata.ini
EOF
