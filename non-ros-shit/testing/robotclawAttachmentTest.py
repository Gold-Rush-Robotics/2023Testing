from roboclaw_python_library.roboclaw_python.roboclaw_3 import Roboclaw

import digitalio
import board


# address = 0x80
address = 131

roboclaw = Roboclaw("/dev/ttyS0", 38400)
roboclaw.Open()


input("input to start")

enablePin = digitalio.DigitalInOut(board.D20)
enablePin.direction = digitalio.Direction.OUTPUT

enablePin = False

roboclaw.ForwardM1(address=address, val=254)

input("input to stop")


roboclaw.ForwardM1(address=address, val=0)

input("input to reverse")

roboclaw.BackwardM1(address=address, val=254)

input("input to stop")


roboclaw.BackwardM1(address=address, val=0)