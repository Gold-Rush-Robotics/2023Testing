import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from time import sleep
import os

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

spi.max_speed_hz = 5_000

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D4)
cs.direction = digitalio.Direction.OUTPUT
reference_voltage = 5.0

#create the mcp object
mcp = MCP.MCP3008(spi, cs, reference_voltage)

print(mcp.reference_voltage)

# create an analog input channel  
adc_channel = AnalogIn(mcp, MCP.P0)

while True:
    print(f"chan: {adc_channel.value} - {adc_channel.voltage:.4f}V")
    sleep(0.1)
