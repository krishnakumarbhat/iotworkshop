# Importing necessary libraries
from machine import Pin, Timer
import network
import time
from umqtt.robust import MQTTClient
import sys
import dht

# Initializing the DHT11 Sensor on gpio 4 of pico w
sensor = dht.DHT11(Pin(4))

# Setting up Wi-Fi credentials
WIFI_SSID     = 'abc'
WIFI_PASSWORD = 'asdf1234'

# Function to connect to Wi-Fi network
def connect_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.disconnect()
    wifi.connect(WIFI_SSID,WIFI_PASSWORD)
    if not wifi.isconnected():
        print('connecting..')
        timeout = 0
        while (not wifi.isconnected() and timeout < 5):
            print(5 - timeout)
            timeout = timeout + 1
            time.sleep(1) 
    if(wifi.isconnected()):
        print('connected')
    else:
        print('not connected')
        sys.exit()

# Call the connect_wifi function to initiate the Wi-Fi connection
connect_wifi() # Connecting to WiFi Router 
# Setting up MQTT credentials
mqtt_client_id      = 'client_'+'123456789' # Just a random client ID
ADAFRUIT_IO_URL     = 'io.adafruit.com' 
ADAFRUIT_USERNAME   = "krishk"
ADAFRUIT_IO_KEY     = "aio_BuyA09Kt7hfRix8aqfOhnJIScGxH"
TEMP_FEED_ID        = 'temp'
HUM_FEED_ID         = 'hum'

# Set up MQTT client and connect to the server
client = MQTTClient(client_id=mqtt_client_id, server=ADAFRUIT_IO_URL, user=ADAFRUIT_USERNAME, password=ADAFRUIT_IO_KEY,ssl=False)

try:            
    client.connect()
except Exception as e:
    print('could not connect to MQTT server {}{}')
    sys.exit()

# Format the feed IDs for temperature and humidity 
temp_feed = bytes(f'{ADAFRUIT_USERNAME}/feeds/{TEMP_FEED_ID}', 'utf-8')
hum_feed = bytes(f'{ADAFRUIT_USERNAME}/feeds/{HUM_FEED_ID}', 'utf-8')

# Function to read sensor data and publish it to the MQTT server
def sens_data(data):
    sensor.measure()                    # Measuring 
    temp = sensor.temperature()         # getting Temp
    hum = sensor.humidity()
    client.publish(temp_feed,    
                  bytes(str(temp), 'utf-8'),   # Publishing Temp feed to adafruit.io
                  qos=0)
    
    client.publish(hum_feed,    
                  bytes(str(hum), 'utf-8'),   # Publishing Hum feed to adafruit.io
                  qos=0)
    print("Temp - ", str(temp))
    print("Hum - " , str(hum))
    print('Msg sent')

# Set up a timer to call the sens_data function every 5 seconds
timer = Timer(-1)
timer.init(period=5000, mode=Timer.PERIODIC,callback=sens_data)
