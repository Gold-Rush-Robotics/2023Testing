from roboclaw_python_library.roboclaw_python.roboclaw_3 import Roboclaw

import digitalio
import board

import numpy as np

from time import perf_counter_ns

def normalize(speed):
    return max(min(speed, 0.99), -0.99)

class Drivetrain:
    def __init__(self):
        self.roboclaw = Roboclaw("/dev/ttyS0", 38400)
        self.roboclaw.Open()

        self.motors = { 
            "fr": Motor(129, True, self.roboclaw),
            "fl": Motor(130, False, self.roboclaw),
            "br": Motor(129, False, self.roboclaw),
            "bl": Motor(130, True, self.roboclaw)
        }
        #self.motors["bl"].reverse(True)
        self.motors["fr"].reverse(True)
        self.motors["fl"].reverse(True)
        

        enablePin = digitalio.DigitalInOut(board.D16)
        enablePin.direction = digitalio.Direction.OUTPUT
        enablePin = False
    
    def driveM(self, fl, fr, bl, br):
        self.motors["fl"].move(int(normalize(fl)*127))
        self.motors["fr"].move(int(normalize(fr)*127))
        self.motors["bl"].move(int(normalize(bl)*127))
        self.motors["br"].move(int(normalize(br)*127))
    
    def driveMecanum(self, forward, strafe, rotate):
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

        self.driveM(powerFL, powerFR, powerBL, powerBR)
    
    def getVoltage(self):
        address = [129, 130]
        voltages = []
        for addy in address:
            vbat = self.roboclaw.ReadMainBatteryVoltage(addy)
            if vbat[0] == 1:
                voltages.append(vbat[1]*.0993)
        
        return sum(voltages)/len(voltages)

    def getCellVoltage(self):
        return self.getVoltage() / 3

class Motor:
    def __init__(self, address, m1, roboclaw):
        self.roboclaw = roboclaw
        print(self.roboclaw.GetConfig(address))
        self.address = address
        self.m1 = m1
        self.reversed = False
        
    def reverse(self, reversed:bool):
        self.reversed = reversed
    
    def move(self, power):
        if((power >= 0 and not self.reversed) or (power <= 0 and self.reversed)):
            self.forward(abs(power))
        else:
            self.backward(abs(power))
            
    def forward(self, power):
        if self.m1:
            self.roboclaw.ForwardM1(self.address, power)
        else:
            self.roboclaw.ForwardM2(self.address, power)
    
    def backward(self, power):
        if self.m1:
            self.roboclaw.BackwardM1(self.address, power)
        else:
            self.roboclaw.BackwardM2(self.address, power)
    
    

if __name__ == "__main__":
    drivetrain = Drivetrain()
    
    while True:
        motor = input("select a motor")
        drivetrain.motors[motor].move(80)
        input("stop")
        drivetrain.motors[motor].move(0)
