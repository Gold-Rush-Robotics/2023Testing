from adafruit_pca9685 import PCA9685
import digitalio
from board import SCL, SDA
import board
import busio
from roboclaw_python_library.roboclaw_python.roboclaw_3 import Roboclaw
import time


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

#luke code :tm:
def lower():
    for i in range(4850, 2500, -10):
        print(i)
        pca.channels[0].duty_cycle = int(i)
        time.sleep(.01)

def higher():
    for i in range(1800, 4850, 10):
        print(i)
        pca.channels[0].duty_cycle = int(i)
        time.sleep(.01)



#7478
#2251

"""
Port 5: Grabber - open: 2251 closed: 7478
Port 1: Cube Grabber - open:6050 closed: 3200 mid:4250
Port 0: lowerer - open: 4850 closed: 1490 partially: 2850
Port 3: bridge - open:7500 closed:8000 hand open: 7700
Port 4: cube flipper - down: 6600, up: 2000
"""
flag = False


while True:
    val = input("Port,Position: ")
    if val == "sweep":
        sweep()
    elif val == "mag":
        print("engaged" if flag else "disengaged")
        if flag:
            roboclaw.ForwardM1(131, 50)
            flag = False
        else:
            flag = True
            roboclaw.ForwardM1(131, 0)
    elif val == "lower":
        lower()
    elif val == "higher":
        higher()
    else:
        pca.frequency = 50
        try:
            port, val = val.split(",")
            port = int(port)
            val = int(val)
            pca.channels[port].duty_cycle = val
        except:
            pass
            
