from roboclaw_python_library.roboclaw_python.roboclaw_3 import Roboclaw

from time import sleep

addresses = [0x81, 0x82]
roboclaw = Roboclaw("/dev/ttyS0", 38400)
roboclaw.Open()

while True:
    
    for address in addresses:
        print(address)
        roboclaw.ForwardM1(address,64)
        roboclaw.ForwardM2(address,64)
        sleep(1)
        roboclaw.ForwardM1(address,0)
        roboclaw.ForwardM2(address,0)
        sleep(1)
        
    


