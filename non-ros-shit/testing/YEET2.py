from drivetraintest import Drivetrain
import digitalio
import board
import time

d = Drivetrain()

input("Enter to Arm")

enablePin = digitalio.DigitalInOut(board.D16)
enablePin.direction = digitalio.Direction.OUTPUT
enablePin.value = False

input("Enter to yeet")
'''
d.driveMecanum(0, 0, -0.5)
time.sleep(0.5)
d.driveMecanum(0, 0, 0.5)
time.sleep(0.6)
d.driveMecanum(1, 0, 0)
#d.driveMecanum(1, 0, 0)
'''
#d.driveMecanum(0.5, -0.5, 0)
#time.sleep(1)
d.driveMecanum(1, 0, 0)

''' #wedge centering
d.driveMecanum(0, -0.5, 0)
time.sleep(1)
d.driveMecanum(0, 0.5, 0)
time.sleep(0.2)
d.driveMecanum(0,0,0)
'''
'''dum stuff i'm trying
d.driveMecanum(0, -0.5, 0)
time.sleep(0.1)
d.driveMecanum(0, .5, 0)
time.sleep(0.1)
d.driveMecanum(1, 0, 0)
'''

''' diagonal ramp jump
d.driveMecanum(1, 0, 0)
time.sleep(1)
d.driveMecanum(1, 0, -0.5)
time.sleep(0.2)


d.driveMecanum(1, -1, 0)
'''



"""
d.driveMecanum(0, 0, .5)#left
time.sleep(0.5)
d.driveMecanum(0.5, 0, 0)#forward
time.sleep(0.25)
d.driveMecanum(0, 0,-.5)#right
time.sleep(.7)
d.driveMecanum(.5, 0, 0)#forward
"""
input("Enter to stop!!!")

enablePin.value = True

d.driveM(0, 0, 0, 0)


