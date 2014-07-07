#!/usr/bin/env python

from Maestor import maestor
import time

robot = maestor()

def cymbalReady():
    robot.setProperty("RSP", "position", -0.8)
    robot.setProperty("RSR", "position", -0.15)
    robot.setProperty("RSY", "position", .5)
    robot.setProperty("REP", "position", -0.7)
    robot.setProperty("RWY", "position", 1.45)
    robot.waitForJoint("RSP")
    robot.setProperty("RWP", "position", 0.6)

if __name__ == "__main__":
    cymbalReady()

