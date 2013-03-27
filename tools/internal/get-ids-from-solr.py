import itertools
import solr
import sys

def main(count):
    s = solr.SolrConnection('http://localhost:8080/solr')
    response = s.query('*:*', fields='id', rows='50000')
    print len(response.results)
    print response.header
    for (cnt,rslt) in itertools.imap(None, xrange(count), response.results):
        print rslt['id']


if __name__ == '__main__' :
    main(int(sys.argv[1]))
