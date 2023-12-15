import board
import busio
import time
import digitalio


import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

from roboclaw_python_library.roboclaw_python.roboclaw_3 import Roboclaw

left_address = 0x81
right_address = 0x82
 
roboclaw = Roboclaw("/dev/ttyS0", 38400)
roboclaw.Open()


enablePin = digitalio.DigitalInOut(board.D20)
enablePin.direction = digitalio.Direction.OUTPUT

enablePin = False

def spinMotor(address:int, m1:bool, speed:float):
    if(m1):
        if(speed >= 0):
            roboclaw.ForwardM1(address, abs(speed)*127)
        else:
            roboclaw.BackwardM1(address, abs(speed)*127)
    else:
        if(speed >= 0):
            roboclaw.ForwardM2(address, abs(speed)*127)
        else:
            roboclaw.BackwardM2(address, abs(speed)*127)

def drivePowers(fl, fr, bl, br):
    spinMotor(left_address, True, fl)
    spinMotor(left_address, False, bl)
    spinMotor(right_address, True, fr)
    spinMotor(right_address, False, br)

def driveMecanum(forward, strafe, rotate):
    powerFL = forward + strafe - rotate
    powerFR = forward - strafe + rotate
    powerBL = forward - strafe - rotate
    powerBR = forward + strafe + rotate
    powerMax = max(abs(powerBL), abs(powerFR), abs(powerFL), abs(powerBR))
    if powerMax >= 1.0:
        powerFL /= powerMax
        powerFR /= powerMax
        powerBL /= powerMax
        powerBR /= powerMax

    drivePowers(powerFL, powerFR, powerBL, powerBR)

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1015(i2c)

# Create single-ended input on channel 0
chan1 = AnalogIn(ads, ADS.P0)
chan2 = AnalogIn(ads, ADS.P1)
chan3 = AnalogIn(ads, ADS.P2)

while True:
    print("{:>5}\t{:>5.3f}".format(chan1.value, chan1.voltage))
    print("{:>5}\t{:>5.3f}".format(chan2.value, chan2.voltage))
    print("{:>5}\t{:>5.3f}".format(chan3.value, chan3.voltage))
    
    forward = (chan1.voltage / 2.5) - 1
    strafe = (chan2.voltage / 2.5) - 1
    rotate = (chan3.voltage / 2.5) - 1
    

    driveMecanum(forward, strafe, rotate)