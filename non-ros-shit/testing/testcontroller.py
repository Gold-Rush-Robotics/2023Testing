from evdev import InputDevice, categorize, ecodes
from drivetraintest import Drivetrain

import numpy as np
import os

print("ACGAM R1 - pad mapping")

#creates object 'gamepad' to store the data
gamepad = InputDevice('/dev/input/event3')

Lu = 127
Ll = 127
Ru = 127
Rl = 127

drive = Drivetrain()


for event in gamepad.read_loop():
    if event.type == 3:
        if(event.code == 00):
            val = event.value
            Ll = val
            #print(f"Left stick up? {val}")
        elif(event.code == 1):
            val = event.value
            Lu = val
            #print(f"Left stick Left? {val}")
        elif(event.code == 4):
            val = event.value
            Ru = val
            #print(f"Right stick up? {val}")
        elif(event.code == 3):
            val = event.value
            Rl = val
            #print(f"Right stick Left? {val}")
            
    forward_shift = Lu - 127
    forward_normalize = (forward_shift) / 127
    forward = -1 * min(max(forward_normalize, -1), 1)
    strafe = min(max((Ll - 127) / 127, -1), 1)
    rotate = min(max((Rl - 127) / 127, -1), 1)
    
    drive.driveMecanum(forward, strafe, rotate)
    
    """os.system("clear")
    print(f"Left:\n\tSide:{Ll}\n\tUp{Lu}")
    print(f"Right:\n\tSide:{Rl}\n\tUp{Ru}")"""
    print(f"forward: {forward}, strafe{strafe}, rotate:{rotate}")
    """print(f"forward shift: {forward_shift}, forward norm: {forward_normalize}")"""
    
    