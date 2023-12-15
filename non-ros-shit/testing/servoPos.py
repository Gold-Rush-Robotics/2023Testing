from adafruit_pca9685 import PCA9685
import digitalio
from board import SCL, SDA
import board
import busio
from roboclaw_python_library.roboclaw_python.roboclaw_3 import Roboclaw
import readline  # Import readline module

i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)

roboclaw = Roboclaw("/dev/ttyS0", 38400)
roboclaw.Open()

# Enable history navigation
readline.parse_and_bind('set editing-mode vi')
readline.parse_and_bind('"\\e[A": history-search-backward')

def custom_input(prompt=''):
    user_input = input(prompt)
    return user_input

def sweep():
    for i in range(50, 330, 10):
        pca.frequency = i
        for j in range(0, 0xFFFF):
            for k in range(7):
                print(f"Frequency: {i} Position: {j} Port: {k}")
                pca.channels[k].duty_cycle = j

flag = False

while True:
    try:
        val = custom_input("Setting: ")  # Use custom_input instead of input
    except KeyboardInterrupt:
        print("\nExiting.")
        break

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
    else:
        pca.frequency = 50
        try:
            port, val = val.split(",")
            port = int(port)
            val = int(val)
            pca.channels[port].duty_cycle = val
        except ValueError:
            pass
