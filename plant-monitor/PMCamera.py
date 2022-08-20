# -*- coding: utf-8 -*-
import time
import picamera

log = open('/home/pi/plant-monitor/logs/PMLog.txt', 'a')

class PMCamera:


    def __init__(self):
        print("Loading camera class")

    def takePic(self):
        print(time.strftime("%m/%d/%Y %I:%M:%S %p") + " - PMCamera: Taking picture")
        log.write("\n" + time.strftime("%m/%d/%Y %I:%M:%S %p") + " - PMCamera: Taking picture")
        log.flush()
        #TAKE PICTURE HERE
        camera = picamera.PiCamera()
        camera.resolution = (1024, 768)
        camera.rotation = 270
        camera.capture('/home/pi/plant-monitor/images/image' + time.strftime("%m_%d_%Y_%I_%M_%S_%p") + '.png')
        camera.capture('/var/www/html/images/image.png')
        camera.close()
        print(time.strftime("%m/%d/%Y %I:%M:%S %p") + " - PMCamera: Picture taken")
        log.write("\n" + time.strftime("%m/%d/%Y %I:%M:%S %p") + " - PMCamera: Picture taken")
