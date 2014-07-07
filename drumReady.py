#!/usr/bin/env python

from Maestor import maestor
import time

robot = maestor()
#EP SP SR SY WY WP

def hitReady():
    robot.setProperties("RWY LWY", "position position", "1.45 -1.28")
    robot.setProperties("RWP LWP", "position position", "0 0")
    robot.waitForJoint("RWP")
    robot.setProperties("RSP LSP", "position position", "-.7 -.8")
    robot.setProperties("RSR LSR", "position position", "0 -.1")
    robot.setProperties("RSY LSY", "position position", ".5 -.5")
    robot.setProperties("REP LEP", "position position", "-.7 -.7")

def hitLeft():
    waitForJoints()
    robot.setProperty("LWY", "velocity", 1)
    robot.setProperty("LWY", "position", -1.38)
    time.sleep(.1)
    robot.setProperty("LWY", "position", -1.28)

def hitRight():
    waitForJoints()
    robot.setProperty("RWY", "velocity", 1)
    robot.setProperty("RWY", "position", 1.55)
    time.sleep(.1)
    robot.setProperty("RWY", "position", 1.45)

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

if __name__ == "__main__":
    main()

