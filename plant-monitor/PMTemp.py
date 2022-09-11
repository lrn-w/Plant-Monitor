# -*- coding: utf-8 -*-
import time
import random
import MySQLdb
import Adafruit_DHT

temp = 0
log = open('/home/pi/plant-monitor/logs/PMLog.txt', 'a')

class PMTemp:

    def __init__(self, pmMessage, TEMP_High, TEMP_Low):
        print("Loading temp class")
        self.pmMessage = pmMessage
        self.tmpHigh = TEMP_High
        self.tmpLow = TEMP_Low

    def getTemp(self):
        print(time.strftime("%m/%d/%Y %I:%M:%S %p") + " - PMTemp: Reading temperature")
        log.write("\n" + time.strftime("%m/%d/%Y %I:%M:%S %p") + " - PMTemp: Reading temperature")
        log.flush()
        #GET TEMP HERE
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11,17)
        temperature = temperature * 9/5.0 + 32
        if humidity is not None and temperature is not None:
            temp = "{0:0.1f}".format(temperature)  #random.uniform(68.0, 93.0)  #91
            humid = "{0:0.1f}".format(humidity)

            #print(str(temperature) + " >= " + str(self.tmpHigh))
        if temperature >= self.tmpHigh:
            print(time.strftime("%m/%d/%Y %I:%M:%S %p") + " - PMTemp: WARNING HIGH Temp Alert! ")
            log.write("\n" + "Temp HIGH warning: The temperature is currently " + str(temp) + " degrees!  " + time.strftime("%m/%d/%Y %I:%M:%S %p"))
            log.flush()
            self.pmMessage.sendMessage("Temp HIGH warning", "The temperature is currently " + str(temp) + " degrees! \r\n " + time.strftime("%m/%d/%Y %I:%M:%S %p"))
        if temperature <= self.tmpLow:
            print(time.strftime("%m/%d/%Y %I:%M:%S %p") + " - PMTemp: WARNING LOW Temp Alert! ")
            log.write("\n" + "Temp LOW warning: The temperature is currently " + str(temp) + " degrees! " + time.strftime("%m/%d/%Y %I:%M:%S %p"))
            log.flush()
            self.pmMessage.sendMessage("Temp LOW warning", "The temperature is currently " + str(temp) + " degrees! \r\n " + time.strftime("%m/%d/%Y %I:%M:%S %p"))
        return temp,humid
