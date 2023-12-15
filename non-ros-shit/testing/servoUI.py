import tkinter as tk
import threading
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

class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GRR Servos")

        self.button_values = {
            "Lifter Up": 4800, "Lifter Down": 1490, "Lifter Middle": 2850,
            "Cube Grabber Open": 5800, "Cube Grabber Close": 3200, "Cube Grabber Fuel Position": 4250,
            "Fuel Tank Open": 2251, "Fuel Tank Closed": 7478,
            "Bridge Load": 7700, "Bridge Closed": 7500, "Bridge Open": 8000,
            "Wedge Up": 2000, "Wedge Down": 6600
        }

        # Dictionary to store port values for each row
        self.row_ports = {
            "Lifter": 0,
            "Cube": 1,
            "Fuel": 5,
            "Bridge": 3,
            "Wedge": 4
        }

        # Dictionary to store current values for each port
        self.port_values = {port: 0 for port in self.row_ports.values()}

        # Create labels to display current values for each port
        self.port_labels = {port: tk.Label(root, text=f"Port {port}: 0") for port in self.row_ports.values()}
        for i, label in enumerate(self.port_labels.values()):
            label.grid(row=i, column=len(self.button_values)//2+1, padx=1, pady=1)

        row_buttons = {}
        for name, value in self.button_values.items():
            row_name = name.split()[0]  # Extract the row name from the button name
            if row_name not in row_buttons:
                row_buttons[row_name] = []

            button = tk.Button(root, text=name, command=lambda name=name, value=value, row_name=row_name: self.button_click(name, value, row_name))
            row_buttons[row_name].append(button)

        # Add Magnet On and Magnet Off buttons
        magnet_on_button = tk.Button(root, text="Magnet On", command=self.magnet_on)
        magnet_off_button = tk.Button(root, text="Magnet Off", command=self.magnet_off)

        lower_button = tk.Button(root, text="Lower Lift", command=self.lower)
        

        # Place buttons on the grid based on rows
        for i, (row_name, buttons) in enumerate(row_buttons.items()):
            for j, button in enumerate(buttons):
                button.grid(row=i, column=j, padx=5, pady=5)

        # Place Magnet buttons in a new row
        magnet_on_button.grid(row=0, column=4, padx=5, pady=5)
        magnet_off_button.grid(row=0, column=5, padx=5, pady=5)

        lower_button.grid(row=0, column=6, padx=5, pady=5)

        self.update_console()

    def button_click(self, button_name, button_value, row_name):
        port = self.row_ports.get(row_name, "N/A")  # Get the port value for the row
        self.port_values[port] = button_value  # Update the current value for the port
        print(f"{button_name} pressed, Value: {button_value}, Port: {port}")
        self.update_port_labels()

    def update_port_labels(self):
        for port, value in self.port_values.items():
            self.port_labels[port].config(text=f"Port {port}: {value}")

    def update_console(self):
        threading.Timer(0.05, self.update_console).start()
        for port, value in self.port_values.items():
            # print(f"Port: {port}, Current Value: {value}")
            # run the pwm thingy
            pca.frequency = 50
            pca.channels[int(port)].duty_cycle = int(value)

    # Functions for Magnet On and Magnet Off
    def magnet_on(self):
        roboclaw.ForwardM1(131, 50)

    def magnet_off(self):
        roboclaw.ForwardM1(131, 0)

    def lower(self):
        for i in range(4800, 2500, -10):
            print(i)
            pca.channels[0].duty_cycle = int(i)
            time.sleep(.01)

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()
