''' 
This script requires the bbs.sqlite database, which can be generated
by the EcoData Retriever:

retriever install bbs -e s -f bbs.sqlite
''' 
import sqlite3 as dbapi
import csv
import sys

try: group = sys.argv[1]
except: group = 'bbs'

con = dbapi.connect('%s.sqlite' % group)
query = open('%s_trait_query.sql' % group).read()
cur = con.cursor()
cur.execute(query)

with sys.stdout as output_file:
    writer = csv.writer(output_file)
    for row in cur:
        writer.writerow(row)