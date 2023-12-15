import board
from board import SCL, SDA
import digitalio
import busio
from adafruit_pca9685 import PCA9685

from drivetraintest import Drivetrain

enablePin = digitalio.DigitalInOut(board.D20)
enablePin.direction = digitalio.Direction.OUTPUT

enablePin.value = True

drivetrain = Drivetrain()

drivetrain.driveM(0, 0, 0, 0)


