# Please note, this code has been adapted from: https://www.raspberrypi.org/blog/monitor-air-quality-with-a-raspberry-pi/

from auth import databaseUser, databasePassword, databaseHost, database
import serial, time
import csv
import datetime
import mysql.connector

# Sleep for two minutes to let sensor warm up
time.sleep(120)

# This connects to the database with given information 
cnx = mysql.connector.connect(user=databaseUser,
                              password=databasePassword,
                              host=databaseHost,
                              database=database)

# Gets a cursor - to send commands to the database
cur = cnx.cursor()

sensor = serial.Serial("/dev/ttyUSB0")

# An infinite loop
while True:
    # Reading bytes off the sensor 
    data = []
    for number in range(0,10):
        byte = sensor.read()
        data.append(byte)

    # Converting the bytes for PM 2.5 and 10 into integer data 
    pmtwofive = int.from_bytes(b''.join(data[2:4]), byteorder="little") /10
    pmten = int.from_bytes(b''.join(data[4:6]), byteorder="little") / 10
    timestamp = datetime.datetime.now()

    # Saving integer data to a named csv file in a speciifed location 
    with open("/home/pi/Desktop/home_air_qual_publishdata.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([timestamp, pmtwofive, pmten])
    
    # This writes to the SDS011SensorDB database
    timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    insertStatement = "insert into pmData(datetime, pmtwofive, pmten) values (\"" + timestamp + "\", " + str(pmtwofive) + ", " + str(pmten) + ");"
    cur.execute(insertStatement)
    cnx.commit()

    # Readings are taken every 60 seconds 
    time.sleep(60)
