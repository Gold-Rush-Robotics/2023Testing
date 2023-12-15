from adafruit_pca9685 import PCA9685
import digitalio
from board import SCL, SDA
import board
import busio
from roboclaw_python_library.roboclaw_python.roboclaw_3 import Roboclaw


i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)

roboclaw = Roboclaw("/dev/ttyS0", 38400)
roboclaw.Open()



def sweep():
    for i in range(50, 330, 10):
        pca.frequency = i
        
        for j in range(0, 0xFFFF):
            
            for k in range(7):
                print(f"Frequency: {i} Position: {j} Port: {k}")
                pca.channels[k].duty_cycle = j


#7478
#2251

"""
Grabber - open: 2251 closed: 7478
Cube Grabber - open:6050 closed: 3000
lowerer - open: 5100 closed: 1490 partially: 4000
"""
flag = False
pca.frequency = 50

while True:
        input()
        print(1490 if flag else 5100)
        pca.channels[2].duty_cycle = 1490 if flag else 5100
        flag = not flag