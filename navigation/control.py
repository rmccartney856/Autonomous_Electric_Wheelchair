#NAME: move.py
#DATE: 12/11/2018
#AUTH: Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC: A python class for moving the wheelchair in an intuative manner
#COPY: Copyright 2018, All Rights Reserved, Ryan McCartney

import numpy as np
import time
import urllib
import requests

class Control:

    #Received Variables
    batteryVoltage = 0
    rightMotorCurrent = 0
    leftMotorCurrent = 0
    status = "NULL"

    #Intrinsic Parameters
    setSpeed = 0
    setAngle = 0
    command = "SEND"

    def __init__(self,host):

        self.host = host

        #Create a file for both transmission and receive logs depending on time
        currentDateTime = time.strftime("%d%m%Y-%H%M%S")
        filename = "data\control\Transmitted Data -" + currentDateTime + ".csv"
        self.transmitLog = open(filename,"w+")
        self.transmitLog.write("Date and Time,Speed,Angle,Command Message\n")

        #Initialise Receive Log
        filename = "data\control\Received Data -" + currentDateTime + ".csv"
        self.receiveLog = open(filename,"w+")
        self.receiveLog.write("Date & Time,Battery Voltage(V),Right Current (A),Left Current (A),Status Message\n")

        #Send Message and Retrieve Response
        self.transmitCommand(0,0,self.command)

    #Send and Receive Messages with implemented logging
    def transmitCommand(self, speed, angle, command):

        #Create form of the payload
        payload = "?serialData="+str(speed)+","+str(angle)+","+command
        
        #combine with host address
        message = self.host + payload

        #Send Message and Retrieve Response
        receivedMessage = requests.get(message)

        #Get Date and Time for Log
        currentDateTime = time.strftime("%d%m%Y-%H%M%S")

        #Write log entry regarding data transmitted
        dataEntry = currentDateTime + "," + speed + "," + angle + "," + command + "\n"
        self.transmitLog.write(dataEntry)
     
        #Write log entry regarding response
        dataEntry = currentDateTime + "," + receivedMessage + "\n"
        self.receiveLog.write(dataEntry)

        self.decodeResponse(receivedMessage)

        setSpeed = speed
        setAngle = angle

    #parse response
    def decodeResponse(self, receivedMessage):
        
        data = receivedMessage.split(",")

        self.batteryVoltage = data[0]
        self.rightMotorCurrent = data[1]
        self.leftMotorCurrent = data[2]
        self.status = data[3]

    #Speed Ramping Function   
    def rampSpeed(self,speed,acceleration):
         
        delay = 1/acceleration
        
        #Direction Forward
        if speed > 0:
            
            #Accelerate
            if speed > self.setSpeed:

                while speed != self.setSpeed:
            
                    speed = self.setSpeed + 1
                    time.sleep(delay)
                    self.transmitCommand(speed,self.setAngle,self.command)

            #Decelerate
            elif speed < self.setSpeed:

                while speed != self.setSpeed:
            
                    speed = self.setSpeed - 1
                    time.sleep(delay)
                    self.transmitCommand(speed,self.setAngle,self.command)

        #Direcion Reverse
        if speed < 0:
            
            #Accelerate
            if speed < self.setSpeed:

                while speed != self.setSpeed:
            
                    speed = self.setSpeed - 1
                    time.sleep(delay)
                    self.transmitCommand(speed,self.setAngle,self.command)

            #Decelerate
            elif speed > self.setSpeed:

                while speed != self.setSpeed:
            
                    speed = self.setSpeed + 1
                    time.sleep(delay)
                    self.transmitCommand(speed,self.setAngle,self.command)

        return speed
    