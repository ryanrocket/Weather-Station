## Portable Weather Station by Ryan Wans ##
## Usage: Collect and Store data collected from DHT sensor ##

## You can view data on: https://tinyurl.com/y8lo5j59 ##

## Some Sensitive Data Was Removed With Respect To The Owner ##

# IMPORTS #
import Adafruit_DHT
import time
import math
import datetime
import logging
import requests
import json
from time import sleep
from Adafruit_IO import Client, Feed

# GLOBALS #
global dht_sensor
global DHT_PIN
global humidity
global temperature
global now
global url
global ID
global PWD
global creds
global date_str
global action_str
global gofor
global hour
global pic

# IO CLIENT #
ADAFRUIT_IO_KEY = 'UNDISCLOSED'
ADAFRUIT_IO_USERNAME = 'UNDISCLOSED'

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
## FEEDS UNDISCLOSED ##
hour = []

# VARIABLES #
dht_sensor = Adafruit_DHT.DHT22
now = datetime.datetime.now()
welcome = ("Welcome Back!")

aio.send(message.key, str(welcome))

DHT_PIN = 4
DELAY_INT = 900

# OUTPUT #
def get():
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(dht_sensor, DHT_PIN)
    
        humidity = round(humidity,2)
        tempc = round(temperature,2)

        tempfu = (tempc * 9/5.0 + 32)
        tempf = round(tempfu,1)
        tempf = tempf - 8.0
    
        logging.basicConfig(filename='data.log',level=logging.DEBUG)

        url = 'https://weatherstation.wunderground.com/UNDISCLOSED'
        ID = 'UNDISCLOSED'
        PWD = 'UNDISCLOSED'
        creds = ('ID=' + ID + "&PASSWORD=" + PWD)
        date_str = "&dateutc=now"
        action_str = "UNDISCLOSED"
        
        def consoleout():
            print("Humidity: ", humidity, " %")
            print("Temperature: ", tempf, " *F")

        def debugout():
            logging.info(now.strftime(" %m-%d %H:%M  > "))
            logging.info(" HUMID: %s P, TEMP: %s *F\n" % (humidity, tempf))

        gofor = (str(url) + str(creds) + str(date_str) + "&humidity=" + str(humidity) + "&tempf=" + str(tempf) + str(action_str))
        r = requests.get(gofor)
        print("Received " + str(r.status_code) + " " + str(r.text))
        aio.send(tem.key, str(tempf))
        aio.send(hum.key, str(humidity))
        consoleout()
        debugout()
        global hour
        hour.append(tempf)
        if len(hour) == 6:
            hour = []
        else:
            if now.strftime("%p") == "PM":
                avg = (sum(hour) / len(hour)) - 0.3
                avg = round(avg, 1)
            elif now.strftime("%p") == "AM":
                avg = (sum(hour) / len(hour)) + 0.3
                avg = round(avg, 1)
            avg = '%DATA%'
            aio.send(prediction.key, str(avg))
        ## ICONS ##
        tempfr = round(tempf, 0)
        tempfr = int(tempfr)
        global pic
        if humidity >= 97:
            pic = 'umbrella'
        else:
            pass
        if tempfr >= 65:
            pic = 'day-sunny'
        elif tempfr >= 48:
            pic = 'thermometer-2'
        elif tempfr >=48 and humidity >=78:
            pic = 'cloud'
        elif tempfr <= 47:
            pic = 'thermometer-1'
        elif tempfr <= 40:
            pic = 'snowflake-o'
        
        aio.send(icon.key, str(pic))
        print("Data List Length: ", len(hour), "\n")
        sleep(DELAY_INT)

def run():
    run = input("Would You Like To Start? (YES/NO) : ")
    if run == "YES":
        get()
    else:
        print("Do 'run()' when ready!")

run()
