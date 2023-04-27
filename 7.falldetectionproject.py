# Import necessary libraries
from machine import Pin, I2C
import time
import math
import network

# Define WiFi network information
ssid = "krishk"  # Enter your WiFi Name
password = "kris1234"  # Enter your WiFi Password

# Function to connect to WiFi
def connect_wifi():
    global ssid, password
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, password)
    while not station.isconnected(): # Loop until WiFi connection is established
        time.sleep(0.5)
        print(".", end="")
    print("\nWiFi connected")

# Define IFTTT Maker Webhooks information
event = "fall_detect"
maker_key = "cMvMC9ExTf9wWFtZqxHEXK1cDEP7eLPWOuqBPfRM0_U"
maker_url = "https://maker.ifttt.com/trigger/" + event + "/with/key/" + maker_key

# Initialize MPU-6050 sensor information
i2c = I2C(0,sda=Pin(4), scl=Pin(5))
MPU_addr = 0x68
i2c.writeto_mem(MPU_addr, 0x6B, bytearray([0]))

# Initialize variables
AcX = AcY = AcZ = GyX = GyY = GyZ = 0.0 
ax = ay = az = gx = gy = gz = 0.0
Amp=0

fall = trigger1 = trigger2 = False
trigger1count = trigger2count = 0
angleChange = 0

# Function to read sensor data
def mpu_read():
    global ax, ay, az, gx, gy, gz
    global AcX,AcY,AcZ,GyX,GyY,GyZ 
    data = i2c.readfrom_mem(MPU_addr, 0x3B, 14)
    AcX = data[0] << 8 | data[1]
    AcY = data[2] << 8 | data[3]
    AcZ = data[4] << 8 | data[5]
    GyX = data[8] << 8 | data[9]
    GyY = data[10] << 8 | data[11]
    GyZ = data[12] << 8 | data[13]

# Function to process sensor data
def data_processing():
    global ax, ay, az, gx, gy, gz
    global AcX,AcY,AcZ,GyX,GyY,GyZ
    global Amp
    ax = (AcX - 2050) / 16384.0
    ay = (AcY - 77) / 16384.0
    az = (AcZ - 1947) / 16384.0
    gx = (GyX + 270) / 131.07
    gy = (GyY - 351) / 131.07
    gz = (GyZ + 136) / 131.07
    Raw_Amp = math.sqrt(ax ** 2 + ay ** 2 + az ** 2)
    Amp = int(Raw_Amp * 10)

# Function to send IFTTT event notification
def send_event(event):
    import urequests
    try:
        urequests.get(maker_url)
        print("IFTTT event sent")
    except:
        print("Failed to send IFTTT event")

connect_wifi()

while True:
    mpu_read()
    data_processing()
    
    #print(Amp)
    
    if Amp <= 2 and not trigger2:
        trigger1 = True
        print("TRIGGER 1 ACTIVATED\n")
        
    if trigger1:
        trigger1count += 1
        if Amp >= 12:
            trigger2 = True
            print("TRIGGER 2 ACTIVATED\n")
            trigger1 = False
            trigger1count = 0
    if trigger2:
        trigger2count += 1
        angleChange = math.sqrt(gx ** 2 + gy ** 2 + gz ** 2)
        #print(angleChange)
        if angleChange >= 30 and angleChange <= 400: #if orientation changes by between 80-100 degrees
            trigger2 = False
            trigger2count = 0
            fall = True            
            
              
    if fall:
        print("FALL DETECTED")
        send_event("fall_detect")
        fall = False
        
    if trigger2count >= 6:
        trigger2 = False
        trigger2count = 0
        print("TRIGGER 2 DECACTIVATED")
        
    if trigger1count >= 6:
        trigger1 = False
        trigger1count = 0
        print("TRIGGER 1 DECACTIVATED")
        
time.sleep(0.1)


