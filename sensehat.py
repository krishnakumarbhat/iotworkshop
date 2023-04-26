#!/usr/bin/python3

import numpy as np
from time import sleep
from sense_hat import SenseHat
import psutil as ps
import time



def clamp(value, min_value, max_value):
    """
    Returns *value* clamped to the range *min_value* to *max_value* inclusive.
    """
    return min(max_value, max(min_value, value))

def scale(value, from_min, from_max, to_min=0, to_max=8):
    """
    Returns *value*, which is expected to be in the range *from_min* to
    *from_max* inclusive, scaled to the range *to_min* to *to_max* inclusive.
    If *value* is not within the expected range, the result is not guaranteed
    to be in the scaled range.
    """
    from_range = from_max - from_min
    to_range = to_max - to_min
    return (((value - from_min) / from_range) * to_range) + to_min

def render_bar(screen, origin, width, height, color):
    """
    Fills a rectangle within *screen* based at *origin* (an ``(x, y)`` tuple),
    *width* pixels wide and *height* pixels high. The rectangle will be filled
    in *color*.
    """
    # Calculate the coordinates of the boundaries
    x1, y1 = origin
    x2 = x1 + width
    y2 = y1 + height
    # Invert the Y-coords so we're drawing bottom up
    max_y, max_x = screen.shape[:2]
    y1, y2 = max_y - y2, max_y - y1
    # Draw the bar
    screen[y1:y2, x1:x2, :] = color

def display_readings(hat, x_range, y_range, z_range):
    """
    Display the temperature, pressure, and humidity readings of the HAT as red,
    green, and blue bars on the screen respectively.
    """

    # Calculate the environment values in screen coordinates

    x_r, y_r, z_r = hat.get_accelerometer_raw().values()
    x = scale(clamp(x_r, *x_range), *x_range)
    y = scale(clamp(y_r, *y_range), *y_range)
    z = scale(clamp(z_r, *z_range), *z_range)

    # Render the bars
    screen = np.zeros((8, 8, 3), dtype=np.uint8)
    render_bar(screen, (0, 0), 2, round(x), color=(110, 0, 0))
    render_bar(screen, (3, 0), 2, round(y), color=(0, 110, 0))
    render_bar(screen, (6, 0), 2, round(z), color=(0, 0, 110))
    hat.set_pixels([pixel for row in screen for pixel in row])
    return x,y,z




def zero_cal():
    return hat.get_accelerometer_raw().values()

def zero_range(zoom, x, y, z):
    xr = (x - zoom, x + zoom)
    yr = (y - zoom, y + zoom)
    zr = (z - zoom, z + zoom)
    return xr, yr, zr


def zoom(scale, x_range, y_range, z_range):
    nx_range = (x_range[0] - scale, x_range[1] + scale)
    ny_range = (y_range[0] - scale, y_range[1] + scale)
    nz_range = (z_range[0] - scale, z_range[1] + scale)
    return nx_range, ny_range, nz_range

def flash(hat, c, sec):
    screen = np.zeros((8, 8, 3), dtype=np.uint8)
    render_bar(screen, (0, 0), 8, 8, color=c)
    hat.set_pixels([pixel for row in screen for pixel in row])
    time.sleep(sec)
    hat.clear()

f = {}
hat = SenseHat()
recording = False
x_zero, y_zero, z_zero = zero_cal()
x_range, y_range, z_range = zero_range(1, x_zero, y_zero, z_zero)
x_range, y_range, z_range = zoom(-0.5, x_range, y_range, z_range)
while True:
    x, y, z = display_readings(hat, x_range, y_range, z_range)
    if recording:
        f.write("{},{},{},{}\n".format(time.time(), x,y,z))
    for event in hat.stick.get_events():
        if event.action == 'pressed' and event.direction == 'up':
            x_range, y_range, z_range = zoom(0.5*(z_range[1]-z_range[0])/2, x_range, y_range, z_range)
        if event.action == 'pressed' and event.direction == 'down':
            x_range, y_range, z_range = zoom(-0.5*(z_range[1]-z_range[0])/2, x_range, y_range, z_range)
        if event.action == 'pressed' and event.direction == 'right':
            if not recording:
                recording = True
                f = open("/home/pi/dat/accel.{}.dat".format(time.time()),"w+")
                f.write("{},{},{},{}\n".format("time", "x","y","z"))
                flash(hat, (155, 0, 0), 0.04)
                flash(hat, (155, 0, 0), 0.04)
                flash(hat, (155, 0, 0), 0.04)
        if event.action == 'pressed' and event.direction == 'left':
            if recording:
                recording = False
                f.close()
                flash(hat, (0, 155, 0), 0.10)
                flash(hat, (0, 155, 0), 0.10)
        if event.action == 'pressed' and event.direction == 'middle':
            old_zoom = (z_range[1]-z_range[0])/2
            time.sleep(3)
            x_zero, y_zero, z_zero = zero_cal()
            x_range, y_range, z_range = zero_range(old_zoom, x_zero, y_zero, z_zero)
