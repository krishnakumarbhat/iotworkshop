# Import necessary libraries
from imu import MPU6050
import time
from machine import Pin, I2C

# Initialize I2C bus
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)

# Create MPU6050 object
imu = MPU6050(i2c)

# Loop continuously to read and print data
while True:
    # Uncomment the following line to print the original data from the library
    # print(imu.accel.xyz,imu.gyro.xyz,imu.temperature,end='\r')
    
    # Round values for a more pretty print
    ax = round(imu.accel.x, 2)
    ay = round(imu.accel.y, 2)
    az = round(imu.accel.z, 2)
    gx = round(imu.gyro.x)
    gy = round(imu.gyro.y)
    gz = round(imu.gyro.z)
    tem = round(imu.temperature, 2)
    
    # Print the rounded values
    print(ax, "\t", ay, "\t", az, "\t", gx, "\t", gy, "\t", gz, "\t", tem, "        ", end="\r")
    
    # Sleep for a short period to allow values to stabilize and be read by a human from the shell
    time.sleep(0.2)
