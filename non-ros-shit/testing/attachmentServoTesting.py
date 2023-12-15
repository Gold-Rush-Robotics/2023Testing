import board
from board import SCL, SDA
import digitalio
import busio
from adafruit_pca9685 import PCA9685

from roboclaw_python_library.roboclaw_python.roboclaw_3 import Roboclaw


address = 0x80

roboclaw = Roboclaw("/dev/ttyS0", 38400)
roboclaw.Open()


def setAll(channels, value: int):
    for channel in channels:
        channel.duty_cycle = int(value)

enablePin = digitalio.DigitalInOut(board.D20)
enablePin.direction = digitalio.Direction.OUTPUT

enablePin = False

i2c = busio.I2C(SCL, SDA)

pca = PCA9685(i2c, address=0x40)

pca.frequency = 300

setAll(pca.channels, 0xAAAA)
roboclaw.ForwardM1(address, 60)

print(pca.channels[0].duty_cycle)

input()

setAll(pca.channels, 0x9111)
roboclaw.BackwardM1(address, 60)
print(pca.channels[0].duty_cycle)

input()

setAll(pca.channels, 0)
roboclaw.ForwardM1(address, 0)
print(pca.channels[0].duty_cycle)
