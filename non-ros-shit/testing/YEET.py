from drivetraintest import Drivetrain
import digitalio
import board

d = Drivetrain()

input("Enter to Arm")

enablePin = digitalio.DigitalInOut(board.D16)
enablePin.direction = digitalio.Direction.OUTPUT
enablePin.value = False

input("Enter to yeet")

d.driveMecanum(0,0 , .50)

try:
    while True:
        ret, m1129, m2129 = d.roboclaw.ReadCurrents(129)
        ret, m1130, m2130 = d.roboclaw.ReadCurrents(130)
        print(f"129 M1: {m1129 / 100 : .3f}A M2: {m2129 / 100 : .2f}A \n130 M1: {m1130 / 100 : .2f}A M2: {m2130 / 100 : .2f}A")
        
except KeyboardInterrupt:
    enablePin.value = True
    d.driveM(0, 0, 0, 0)


