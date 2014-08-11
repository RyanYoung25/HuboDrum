#!/usr/bin/env python

from Maestor import maestor
import time

robot = maestor()
leftBase=0
rightBase=0
leftHit= 0
rightHit= 0

def getStrikes():
    global leftHit
    global rightHit
    global leftBase
    global rightBase
    f = open("cymbalConfig.txt", "r")
    for line in f:
        words = line.split(" ")
        if words[0] == "Left:":
            leftHit = float(words[1])
        elif words[0] == "Right:":
            rightHit = float(words[1])
    leftBase = float(robot.getProperties("LWY", "position"))
    rightBase = float(robot.getProperties("RWY", "position"))



def hitCymbal():
    robot.setProperty("RWY", "position", rightHit)
    time.sleep(.10)
    robot.setProperty("RWY", "position", rightBase)

def hitDrum():
    robot.setProperty("LWY", "position", leftHit)
    time.sleep(.10)
    robot.setProperty("LWY", "position", leftBase)
def play():
    for i in range(0, 30):
        hitCymbal()
        time.sleep(.25)
        hitCymbal()
        time.sleep(.15)
        hitCymbal()
        time.sleep(.15)
        hitDrum()
    

if __name__ == "__main__":
    getStrikes()
    print leftBase
    print rightBase
    print leftHit
    print rightHit
    play()
