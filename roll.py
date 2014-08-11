#!/usr/bin/env python

from Maestor import maestor
import time

leftHit = 0
leftBase = 0
rightHit = 0
rightBase = 0

robot = maestor()
#EP SP SR SY WY WP


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
    leftBase = leftHit + .05 
    rightBase = rightHit - .05
    print leftBase
    print leftHit
    f.close()

def hitReady():
    robot.setProperties("RSP LSP", "position position", "-.7 -.8")
    robot.setProperties("RSR LSR", "position position", "0 -.1")
    robot.setProperties("RSY LSY", "position position", ".5 -.5")
    robot.setProperties("REP LEP", "position position", "-.7 -.7")
    robot.setProperties("RWY LWY", "position position", rightBase + " " + leftBase)
    robot.setProperties("RWP LWP", "position position", "0 0")

def hitLeft():
    waitForJoints()
    robot.setProperty("LWY", "velocity", 2)
    robot.setProperty("LWY", "position", -1.4)
    time.sleep(.05)
    robot.setProperty("LWY", "position", -1.3)

def hitRight():
    robot.setProperty("RWY", "velocity", 3)
    robot.setProperty("LWY", "velocity", 3)
    robot.setProperty("RWY", "position", rightHit)
    time.sleep(.02)
    robot.setProperty("LWY", "position", leftHit)
    robot.setProperty("RWY", "position", rightBase)
    time.sleep(.02)
    robot.setProperty("LWY", "position", leftBase)

def setVelocities():
    robot.setProperties("REP LEP RSP LSP RSR LSR RSY LSY RWY LWY RWP LWP", "velocity velocity velocity velocity velocity velocity velocity velocity velocity velocity velocity velocity", ".3 .3 .3 .3 .3 .3 .3 .3 .3 .3 .3 .3")

def waitForJoints():
    robot.waitForJoint("REP")
    robot.waitForJoint("LEP")
    robot.waitForJoint("RSP")
    robot.waitForJoint("LSP")
    robot.waitForJoint("RSR")
    robot.waitForJoint("LSR")
    robot.waitForJoint("RSY")
    robot.waitForJoint("LSY")
    robot.waitForJoint("RWY")
    robot.waitForJoint("LWY")
    robot.waitForJoint("RWP")
    robot.waitForJoint("LWP")

def main():
    setVelocities()
    hitReady()
    waitForJoints()
    for i in range(0, 50):
        hitRight()


if __name__ == "__main__":
    main()

