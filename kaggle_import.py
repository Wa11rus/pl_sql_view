import csv
import cx_Oracle

username = 'crispyyv'
password = '19680401'
database = 'localhost/xe'

connection = cx_Oracle.connect(username, password, database)
cursor = connection.cursor()

filename = "fire_archive_M6_96619.csv"


connection.commit()
with open(filename, newline='') as file:
    reader = csv.DictReader(file)
    i = 1

    try:

        for el in reader:
            latitude = float(el['latitude'])
            longitude = float(el['longitude'])
            brightness = float(el['brightness'])
            confidence = int(el['confidence'])
            frp = float(el['frp'])

            query = """INSERT INTO locations(location_id, longitude, latitude) VALUES(:location_id, :longitude,
            :latitude) """
            cursor.execute(query, location_id=i, longitude=longitude, latitude=latitude)
            query = """ INSERT INTO params(params_id, brightness, frp) VALUES(:params_id, :brightness, :frp)"""
            cursor.execute(query, params_id=i, brightness=brightness, frp=frp)
            query = """begin INSERT INTO confidence(confidence) VALUES(:confidence); exception when dup_val_on_index then  
            null; END; """
            cursor.execute(query, confidence = confidence)
            query = """INSERT INTO fire_info(fire_id, location_id, params_id, confidence) VALUES(:fire_id,
            :location_id,:params_id,:confidence) """
            cursor.execute(query,fire_id=i, location_id=i,params_id=i, confidence=confidence)
            i += 1

    except:
        raise

connection.commit()
cursor.close()
connection.close()
