#!/usr/bin/env python

import alsaaudio
import sys
import time
import audioop
from Maestor import maestor

robot = maestor()
hitTimes = []
oldTime = time.time()
leftHit = 0
leftBase = 0
rightHit = 0 
rightBase = 0

def startStopTime():
    global oldTime
    currTime = time.time() 
    interval = currTime - oldTime - .1
    if interval > .15:
        oldTime = currTime
        hitTimes.append(interval)
        print hitTimes

def loadJointValues():
    global leftHit
    global rightHit
    global leftBase
    global rightBase
    f = open("hitConfig.txt", "r")
    for line in f:
        words = line.split(" ")
        if words[0] == "Left:":
            leftHit = float(words[1])
        elif words[0] == "Right:":
            rightHit = float(words[1])
    leftBase = leftHit + .05 #float(robot.getProperties("LWY", "position"))
    rightBase = rightHit - .05 #float(robot.getProperties("RWY", "position"))
    print leftBase
    print leftHit
    f.close()

def hitDrum():
    robot.setProperty("LWY", "position", leftHit)
    time.sleep(.1)
    robot.setProperty("LWY", "position", leftBase) 
    
def printHits():
    for i in hitTimes:
        time.sleep(i)
        hitDrum()
        print "Hit!"

def listen():
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
        #Start an big loop that gets and analyzes audio data
        for i in range(0, 5000):
            l, data = audioInput.read()
            if l > 0:
                spike = 0
                lchan = audioop.tomono(data, 2, 1, 0)
                rchan = audioop.tomono(data, 2, 0, 1)
                lmax = audioop.max(lchan, 2)
                rmax = audioop.max(rchan, 2)
                if spike < lmax:
                    spike = lmax
                if spike < rmax:
                    spike = rmax
                
                if spike > 1000:
                    startStopTime()
            time.sleep(.001) #audio refresh rate
    except KeyboardInterrupt :
        sys.exit() #TODO make it actually exit

if __name__ == '__main__':
    loadJointValues()
    listen()
    printHits()            
