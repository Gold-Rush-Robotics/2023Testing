import tkinter as tk
import threading

class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Button Demo")

        self.button_values = {
            "Lifter Up": 4850, "Lifter Down": 1850, "Lifter Middle": 2500,
            "Cube Grabber Open": 1000, "Cube Grabber Close": 2000, "Cube Grabber Fuel Position": 1500,
            "Fuel Tank Open": 1000, "Fuel Tank Closed": 6000,
            "Bridge Load": 1000, "Bridge Closed": 2000, "Bridge Open": 3000,
            "Wedge Up": 2000, "Wedge Down": 3000
        }

        # Dictionary to store port values for each row
        self.row_ports = {
            "Lifter": 0,
            "Cube": 1,
            "Fuel": 2,
            "Bridge": 3,
            "Wedge": 4
        }

        # Dictionary to store current values for each port
        self.port_values = {port: 0 for port in self.row_ports.values()}

        # Create labels to display current values for each port
        self.port_labels = {port: tk.Label(root, text=f"Port {port}: 0") for port in self.row_ports.values()}
        for i, label in enumerate(self.port_labels.values()):
            label.grid(row=i, column=len(self.button_values)//2, padx=5, pady=5)

        row_buttons = {}
        for name, value in self.button_values.items():
            row_name = name.split()[0]  # Extract the row name from the button name
            if row_name not in row_buttons:
                row_buttons[row_name] = []

            button = tk.Button(root, text=name, command=lambda name=name, value=value, row_name=row_name: self.button_click(name, value, row_name))
            row_buttons[row_name].append(button)

        # Place buttons on the grid based on rows
        for i, (row_name, buttons) in enumerate(row_buttons.items()):
            for j, button in enumerate(buttons):
                button.grid(row=i, column=j, padx=5, pady=5)

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
        threading.Timer(0.1, self.update_console).start()
        for port, value in self.port_values.items():
            print(f"Port: {port}, Current Value: {value}")
            # run the pwm thingy

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()
