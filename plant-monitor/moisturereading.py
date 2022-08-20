# file name moisturereading.py
# description - this file contains the implementation to read moisture readings

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
from time import sleep, ctime
import time
import random
import MySQLdb

log = open('/home/pi/plant-monitor/logs/PMLog.txt', 'a')

class MoistureReading:
    def __init__(self, pm_message):        
        # Software SPI configuration:
        self.pm = pm_message
        self.CLK  = 18
        self.MISO = 23
        self.MOSI = 24
        self.CS = 25
        self.mcp_ = Adafruit_MCP3008.MCP3008(clk=self.CLK, cs=self.CS, miso=self.MISO, mosi=self.MOSI)

        # Hardware SPI configuration:
        SPI_PORT   = 0
        SPI_DEVICE = 0
        self.mcp_ = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

    def getMoistureReading(self,temp,humid):
        print(time.strftime("%m/%d/%Y %I:%M:%S %p") + " - Plant Monitor: Reading Soil Moisture")
        log.write("\n" + time.strftime("%m/%d/%Y %I:%M:%S %p") + " - Plant Monitor: Reading temperature")
        log.flush()
        # read moisture content
        value = self.mcp_.read_adc(0)
        if value is not None:
            value = (float(value) / 1023) * 100            
            moisture = "{0:0.1f}".format(value)
            db = MySQLdb.connect("localhost", "pi", "raspberry", "plantmonitor")
            curs = db.cursor()
            try:
                curDate = time.strftime('%Y-%m-%d %H:%M:%S')
                sql = "INSERT INTO PMMoisture VALUES(NULL, '%s', '%s', %s, %s)" % (curDate, moisture,temp,humid)
                curs.execute(sql)
                db.commit()
            except:
                print("PMMoisture: DB comit error, transaction being rolled back")
                db.rollback()
        if value >= 65:
                print(time.strftime("%m/%d/%Y %I:%M:%S %p") + " - PMMoisture: WARNING Dry Soil Alert! ")
                log.write("\n" + "DRY soil Warning: The soil moisture content is currently: " + str(value) + " Temperature is: " + str(temp) + " Humidity is: " + str(humid)  +" " + time.strftime("%m/%d/%Y %I:%M:%S %p"))
                log.flush()
                self.pm.sendMessage("DRY soil warning", "The soil moisture content is currently: " + str(value) + " Temperature is: " + str(temp) + " Humidity is: " + str(humid) +"  \r\n " + time.strftime("%m/%d/%Y %I:%M:%S %p"))
        elif value <= 30:
                print(time.strftime("%m/%d/%Y %I:%M:%S %p") + " - PMMoisture: WARNING Oversatured Soil Alert! ")
                log.write("\n" + "Oversaturated Soil warning: The soil moisture content is currently: " + str(value) + " Temperature is: " + str(temp) + " Humidity is: " + str(humid) + "  " + time.strftime("%m/%d/%Y %I:%M:%S %p"))
                log.flush()
                self.pm.sendMessage("Oversaturated soil warning", "The soil moisture content is currently: " + str(value) + " Temperature is: " + str(temp) + " Humidity is: " + str(humid)  + " \r\n " + time.strftime("%m/%d/%Y %I:%M:%S %p"))

        else:
            print(time.strftime("%m/%d/%Y %I:%M:%S %p") + " - PMMoisture: Soil OK! ")
            log.write("\n" + "Soil OK, The soil moisture content is currently: " + str(value) + " Temperature is: " + str(temp) + " Humidity is: " + str(humid) + "  " + time.strftime("%m/%d/%Y %I:%M:%S %p"))
            log.flush()
            self.pm.sendMessage("Soil OK", "The soil moisture content is currently: " + str(value) + " Temperature is: " + str(temp) + " Humidity is: " + str(humid)  + " \r\n " + time.strftime("%m/%d/%Y %I:%M:%S %p"))
            
        
