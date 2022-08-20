# -*- coding: utf-8 -*-
import time
from PMTemp import PMTemp
from PMCamera import PMCamera
from PMMessage import PMMessage
from moisturereading import MoistureReading

#VARIABLES
pollingInterval = 600  #In seconds
TEMP_High = 80
TEMP_Low = 65
SMS_Notifications = True
pmMessage = PMMessage(SMS_Notifications)
pmTemp = PMTemp(pmMessage, TEMP_High, TEMP_Low)
pmMoisture = MoistureReading(pmMessage)
pmCamera = PMCamera()
log = open('/home/pi/plant-monitor/logs/PMLog.txt', 'a')


#FUNCTIONS
#LOOP
while True:
    print("-------------------------------------")
    print(time.strftime("%m/%d/%Y %I:%M:%S %p") + " - Plant Monitor Started")
    log.write("\n-------------------------------------\n" + time.strftime("%m/%d/%Y %I:%M:%S %p") + " - Plant Monitor Started")
    log.flush()
    temp,humid = pmTemp.getTemp()
    pmMoisture.getMoistureReading(temp,humid)
    pmCamera.takePic()
    print(time.strftime("%m/%d/%Y %I:%M:%S %p") + " - Plant Monitor Completed")
    log.write("\n-------------------------------------\n" + time.strftime("%m/%d/%Y %I:%M:%S %p") + " - Plant Monitor Completed")
    log.flush()
    time.sleep(pollingInterval)