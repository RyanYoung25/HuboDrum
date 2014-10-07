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
    f = open("hitConfig.txt", "r")
    for line in f:
        words = line.split(" ")
        if words[0] == "Left:":
            leftHit = float(words[1])
        elif words[0] == "Right:":
            rightHit = float(words[1])
    leftBase = float(robot.getProperties("LWY", "goal"))
    rightBase = rightHit - .1



def hitCymbal():
    robot.setProperty("RWY", "position", rightHit)
    time.sleep(.10)
    robot.setProperty("RWY", "position", rightBase)

def simHit():
    robot.setProperties("RWY LWY", "position position", str(rightHit) + " " + str(leftHit))
    time.sleep(.10)
    robot.setProperties("RWY LWY", "position position", str(rightBase) + " " + str(leftBase))

def hitDrum():
    robot.setProperty("LWY", "position", leftHit)
    time.sleep(.10)
    robot.setProperty("LWY", "position", leftBase)

def hitCymbalEmp():
    robot.setProperties("RWY RWY", "position velocity", str(rightHit) + " 4")
    time.sleep(.10)
    robot.setProperties("RWY RWY", "position velocity", str(rightBase) + " 2")

def simHitEmp():
    robot.setProperties("RWY LWY RWY LWY", "position position velocity velocity", str(rightHit) + " " + str(leftHit) + " 3 3")
    time.sleep(.10)
    robot.setProperties("RWY LWY RWY LWY", "position position velocity velocity", str(rightBase) + " " + str(leftBase) + " 2 2")

def hitDrumEmp():
    robot.setProperties("LWY LWY", "position velocity", str(leftHit) + " 3")
    time.sleep(.10)
    robot.setProperties("LWY LWY", "position velocity", str(leftBase) + " 2")

def setVelocities():
    robot.setProperties("LWY RWY", "velocity velocity", "2 2")

def beat1():
    for i in range(0, 10):
        hitCymbal()
        time.sleep(.25)
        hitCymbal()
        time.sleep(.15)
        hitCymbal()
        time.sleep(.15)
        hitDrum()

def beat2():
    for i in range(0, 10):
        hitDrum()
        time.sleep(.25)
        hitCymbal()
        time.sleep(.25)
        hitCymbal()
        time.sleep(.15) 

def beat3():
    #going for jazz
    for i in range(0, 10):
        #simHit()
        hitCymbalEmp()
        time.sleep(.4)
        hitCymbal()
        time.sleep(.15)
        hitCymbal()
        time.sleep(.15)

def beat4():
    for i in range(0, 10):
        hitCymbal()
        time.sleep(.1)
        hitDrum()
        time.sleep(.1)
        hitDrum()
        time.sleep(.1)
        hitDrum()
        time.sleep(.1)
        hitDrumEmp()
        time.sleep(.2)
        hitCymbal()
        time.sleep(.1)
        hitDrum()
        time.sleep(.1)


def play():
    beat1()
    beat2()
    beat3()
    #beat4()

if __name__ == "__main__":
    getStrikes()
    setVelocities()
    print leftBase
    print rightBase
    print leftHit
    print rightHit
    play()
