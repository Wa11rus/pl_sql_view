import csv
import cx_Oracle
from datetime import datetime

username = 'crispyyv'
password = '19680401'
database = 'localhost/xe'

connection = cx_Oracle.connect(username, password, database)
cursor = connection.cursor()

filename = "cars_ver2.csv"

with open(filename, newline='') as file:
    reader = csv.DictReader(file)
    i = 1

    try:
        for row in reader:
            title = row['title']
            pub_date = row['pub_date']
            city = row['city']
            region = row['region']
            mark = row['mark']
            model = row['model']
            year = int(row['year'])
            mileage = int(row['mileage'])
            price = int(row['price'])

            insert = """INSERT INTO car ( car_id, model, mark, year, mileage)
                            values (:car_id, :model, :mark, :year, :mileage)"""
            cursor.execute(insert, car_id=i, model=model, mark=mark, year=year, mileage=mileage)
            insert = """INSERT INTO location ( location_id, region, city)
                values (:location_id, :region , :city)"""
            cursor.execute(insert, location_id=i, region=region, city=city)
            insert = """INSERT INTO olx_info ( price, title, pub_date, location_id, car_id)
                values (:price, :title , TO_DATE(:pub_date), :location_id, :car_id)"""
            cursor.execute(insert, price=price, title=title, pub_date=pub_date, location_id=i, car_id=i)

            i += 1

    except:
        print(f"Error in line: {i}")
        raise

connection.commit()
cursor.close()
connection.close()
