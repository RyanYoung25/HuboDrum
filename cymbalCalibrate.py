#!/usr/bin/env python

import alsaaudio
import sys
import time
import audioop
import threading
from Maestor import maestor


robot = maestor()
RightBase = 1.45 #The initial starting value for the Right wrist
LeftBase = -1.28 #The initial starting value for the Left wrist 
hitFound = False
RightStrike = RightBase
LeftStrike = LeftBase


def tryRight():
    global RightStrike
    global RightBase
    robot.setProperty("RWY", "position", RightStrike)
    time.sleep(.25)
    robot.setProperty("RWY", "position", RightBase)

def tryLeft():
    global LeftStrike
    global LeftBase
    robot.setProperty("LWY", "position", LeftStrike)
    time.sleep(.25)
    robot.setProperty("LWY", "position", LeftBase)

def paradiddle():
    for i in range(0, 3):
        tryRight()
        time.sleep(.25)
        tryLeft()
        time.sleep(.25)
       
def roll():
    robot.setProperties("RWY LWY", "velocity velocity", "3 3")
    for i in range(0, 50):
        robot.setProperty("RWY", "position", RightStrike)
        time.sleep(.02)
        robot.setProperty("LWY", "position", LeftStrike)
        robot.setProperty("RWY", "position", RightStrike - .03)
        time.sleep(.02)
        robot.setProperty("LWY", "position", LeftStrike + .03)

    robot.setProperties("RWY LWY", "position position", str(RightBase) + " " + str(LeftBase))

def calibrate():
    global hitFound
    global RightStrike
    global LeftStrike

    configFile = open("cymbalConfig.txt", "w")
    robot.setProperties("RWY LWY", "velocity velocity", "2 2")
    CalibratingRight = True
    CalibratingLeft = True
    while CalibratingRight:
        tryRight()
        time.sleep(2)
        if hitFound:
           print "Hit found"
           CalibratingRight = False
           hitFound = False
        else:
           print "Hit not found"
           RightStrike = RightStrike + 0.01

    while CalibratingLeft:
        tryLeft()
        time.sleep(2)
        if hitFound:
           print "Hit found"
           CalibratingLeft = False
           hitFound = False
        else:
           print "Hit not found"
           LeftStrike = LeftStrike - 0.01


    RightStrike = RightStrike + 0.01
    LeftStrike = LeftStrike - 0.01    
    print "Done Calibrating"
    print "Left Strike is: " + str(LeftStrike)
    print "Right Strike is: " + str(RightStrike)
    configFile.write("Left: " + str(LeftStrike)+ " \n")
    configFile.write("Right: " + str(RightStrike))
    configFile.close()

class listenThread(threading.Thread):
    def __init__(self):
        super(listenThread, self).__init__()

    def run(self):
        global hitFound
        #Initialize and set the properties of PCM object
        card = 'default'
        audioInput = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, card)
        audioInput.setchannels(2)
        audioInput.setrate(44100)
        audioInput.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        audioInput.setperiodsize(160)
        oldL = 1
        oldR = 1
        try:
            #Start an infite loop that gets and analyzes audio data
            count = 0
            spike = 0
            while True:
                l, data = audioInput.read()
                if l > 0:
                    spike = 0
                    lchan = audioop.tomono(data, 2, 1, 0)
                    rchan = audioop.tomono(data, 2, 0, 1)
                    lmax = audioop.max(lchan, 2)
                    rmax = audioop.max(rchan, 2)
                    #print str(lmax) + " " + str(rmax)
                    if spike < lmax:
                        spike = lmax
                    if spike < rmax:
                        spike = rmax
                    #print spike
                    if spike > 1000:
                        hitFound = True
                    time.sleep(.001) #audio refresh rate
        except KeyboardInterrupt :
            sys.exit() #TODO make it actually exit

def main():
    global hitFound
    global RightStrike
    global LeftStrike

    listen = listenThread()
    listen.start()
    calibrate()
    listen.stop()
    sys.exit()

if __name__ == "__main__":
    main()
