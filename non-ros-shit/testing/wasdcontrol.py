from drivetraintest import Drivetrain
import digitalio
import board
import keyboard

d = Drivetrain()

input("Enter to Arm")

enablePin = digitalio.DigitalInOut(board.D16)
enablePin.direction = digitalio.Direction.OUTPUT
enablePin.value = False

input("Enter to yeet")

# Initial values
x = 0
y = 0

# Define a callback function for key presses
def on_key_event(e):
    global x, y
    if e.event_type == keyboard.KEY_DOWN:
        if e.name == 'w':
            y = 0.5  # Increase forward velocity
        elif e.name == 's':
            y = -0.5  # Increase backward velocity
        elif e.name == 'a':
            x = -0.5  # Increase leftward velocity
        elif e.name == 'd':
            x = 0.5  # Increase rightward velocity
    elif e.event_type == keyboard.KEY_UP:
        if e.name in ('w', 's'):
            y = 0  # Stop forward/backward movement
        elif e.name in ('a', 'd'):
            x = 0  # Stop left/right movement

    # Call the driveMecanum function with the updated x and y values
    d.driveMecanum(x, y, 0)  # Assuming 0.5 is a default value for the third parameter

# Register the callback function for key events
while True:
	keyboard.hook(on_key_event)


