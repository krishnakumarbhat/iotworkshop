import machine
import time

# Set up LED pin
led_pin = machine.Pin('LED', machine.Pin.OUT)

# Blink LED
while True:
    led_pin.value(1)  # Turn LED on
    time.sleep(0.5)   # Wait for 500 milliseconds
    led_pin.value(0)  # Turn LED off
    time.sleep(0.5)   # Wait for 500 milliseconds

