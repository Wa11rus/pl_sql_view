import csv

import cx_Oracle

username = 'asd'
password = 'asd'
database = 'localhost/xe'

tables = ['Confidence', 'Fire_info', 'Params', 'Locations']

conn = cx_Oracle.connect(username, password, database)

cursor = conn.cursor()


try:
    for table in tables:
        with open(table+'.csv', 'w', newline='') as newCsvFile:
            cursor.execute("SELECT * FROM " + table)

            titles = []

            for row in cursor.description:
                titles.append(row[0])
            csvWriter=csv.writer(newCsvFile, delimiter=',')
            csvWriter.writerow(titles)

            for row in cursor:
                csvWriter.writerow(row)
finally:
    cursor.close()
    conn.close()
