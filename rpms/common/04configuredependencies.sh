#! /bin/sh
# configure our dependencies (packages which have been installed before)
set -x
if [ -f /tmp/kata-SKIP04 ]
then
  echo "Skipping 04"
  exit 0
fi
patchdir=$1

