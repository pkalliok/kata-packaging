#! /bin/sh
cd rpmbuild/SOURCES
curl -O http://archive.apache.org/dist/lucene/solr/4.0.0/apache-solr-4.0.0.tgz
cd ../SPECS
ln -s ../../rpms/solr/solr.spec
arch=$(rpm -q --qf '%{arch}\n' --specfile solr.spec | head -n 1)
# just in case, make sure the * in yum install command below will not match
# several files
rm -f ../RPMS/${arch}/apache-solr-3.5.0-*.el6.${arch}.rpm
rpmbuild -ba solr.spec
cd ../RPMS/${arch}
sudo yum install -y apache-solr-4.0.0-1.el6.${arch}.rpm
