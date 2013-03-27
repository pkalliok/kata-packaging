# reads ids from a file and inserts them into a DB table called test_ids
#
# Purpose: Comparing contents of Solr index to contents of DB 
#
#          - input file can be created using script get-ids-from-solr.py
#          - resulting test_ids contents can be compared to package(id) 
#            using psql
#
import sqlalchemy
sa = sqlalchemy
import sys

def main(fn):
    eng = sa.create_engine( 'postgresql://ckanuser:cKan0001@localhost/ckantest')
    metadata = sa.MetaData()
    test_ids = sa.Table('test_ids', metadata, sa.Column('id', sa.Text))
    metadata.create_all(eng)
    conn = eng.connect()
    ins = test_ids.insert()
    infile = open(fn, "r")
    for line in infile:
        if line[-1:] == "\n":
            line = line[:-1]
        conn. execute(ins, id = line)


if __name__ == '__main__' :
    main(sys.argv[1])
