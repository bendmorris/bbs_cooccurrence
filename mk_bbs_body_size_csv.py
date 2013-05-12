''' 
This script requires the bbs.sqlite database, which can be generated
by the EcoData Retriever:

retriever install bbs -e s -f bbs.sqlite
''' 
import sqlite3 as dbapi
import csv
import sys

con = dbapi.connect('bbs.sqlite')
query = open('bbs_body_size_query.sql').read()
cur = con.cursor()
cur.execute(query)

with sys.stdout as output_file:
    writer = csv.writer(output_file)
    writer.writerow(('species','m_body_size','unsexed_body_size','m_bill_size','unsexed_bill_size'))
    for row in cur:
        writer.writerow(row)