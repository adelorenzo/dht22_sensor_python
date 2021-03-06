#!/usr/bin/python

import time
import sys
import datetime
import Adafruit_DHT
from influxdb import InfluxDBClient

# Configure InfluxDB connection variables
host = "10.51.1.39" # My Ubuntu NUC
port = 8086 # default port
#user = "rpi-3" # the user/password created for the pi, with write access
#password = "rpi-3" 
dbname = "sensor_data" # the database we created earlier
interval = 2 # Sample period in seconds

# Create the InfluxDB client object
#client = InfluxDBClient(host, port, user, password, dbname)
client = InfluxDBClient(host, port, "", "",  dbname)

# Enter the sensor details
sensor = Adafruit_DHT.DHT22
sensor_gpio = 4

# think of measurement as a SQL table, it's not...but...
measurement = "rpi-dht22"
# location will be used as a grouping tag later
location = "office"

# Run until you get a ctrl^c
try:
    while True:
        # Read the sensor using the configured driver and gpio
        humidity, temperature = Adafruit_DHT.read_retry(sensor, sensor_gpio)
        #iso = time.ctime()
	utc = datetime.datetime.utcnow()
        # Print for debugging, uncomment the below line
        # print("[%s] Temp: %s, Humidity: %s" % (utc, temperature, humidity)) 
        # Create the JSON data structure
        data = [
        {
          "measurement": measurement,
              "tags": {
                  "location": location,
              },
              "time": utc,
              "fields": {
                  "temperature" : temperature,
                  "humidity": humidity
              }
          }
        ]
        # Send the JSON data to InfluxDB
        client.write_points(data)
        # Wait until it's time to query again...
        time.sleep(interval)
 
except KeyboardInterrupt:
    pass
