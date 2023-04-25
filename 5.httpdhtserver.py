import time                # Importing the time module for sleep/delay functionality
import network             # Importing the network module to access Wi-Fi functionality
import socket              # Importing the socket module to implement socket programming
from machine import Pin    # Importing the Pin module from machine for GPIO control
import dht                 # Importing the dht module for DHT sensor functionality

dht_pin = Pin(4, Pin.IN)    # Initializing pin 4 for DHT11 sensor
dht_sensor = dht.DHT11(dht_pin) # Initializing DHT11 sensor object using the pin 4

ssid = 'abc'              # Setting the SSID of the Wi-Fi network to connect
password = 'asdf1234'      # Setting the password of the Wi-Fi network to connect

wlan = network.WLAN(network.STA_IF) # Initializing the Wi-Fi interface
wlan.active(True)           # Enabling the Wi-Fi interface
wlan.connect(ssid, password) # Connecting to the Wi-Fi network

# Wait for connect or fail
max_wait = 10               # Setting a maximum wait time for Wi-Fi connection
while max_wait > 0:         # Looping while the wait time is greater than zero
    if wlan.status() < 0 or wlan.status() >= 3: # Check for Wi-Fi connection status
        break               # If the Wi-Fi connection status is below 0 or above 3, exit the loop
    max_wait -= 1           # Decrement the maximum wait time by 1
    print('waiting for connection...')
    time.sleep(1)           # Delaying execution for 1 second

# Handle connection error
if wlan.status() != 3:      # If the Wi-Fi status is not 3, meaning not connected
    raise RuntimeError('network connection failed') # Raise a runtime error
else:                       # Otherwise, Wi-Fi is connected successfully
    print('Connected')      
    status = wlan.ifconfig()# Get the IP address of the Wi-Fi connection
    print( 'ip = ' + status[0] ) # Print the IP address

# HTML code to be sent to the client
html = """<!DOCTYPE html>                  
<html>
<head> <title>Pico W</title> </head>
<body> <h1>Pico W HTTP Server</h1>
<p>Temperature: {} C</p>
<p>Humidity: {} %</p>
</body>
</html>
"""

# Open socket
addr = socket.getaddrinfo('0.0.0.0',45000)[0][-1] # Get the IP address of the server and port number to bind socket to
s = socket.socket()         # Create a socket object
s.bind(addr)                # Bind the socket object to the IP address and port number
s.listen(1)                 # Listen for incoming connections
print('listening on', addr)

# Listen for connections, serve client
while True:                 # Infinite loop to listen for incoming connections and serve clients
    try:       
        cl, addr = s.accept()    # Accept incoming connection
        print('client connected from', addr)
        request = cl.recv(1024)  # Receive request from the client
        print("request:")
        print(request)
        request = str(request)

        temp = None                 # Initializing temperature variable
        humidity = None             # Initializing humidity variable
        dht_sensor.measure()        # Measuring the temperature and humidity
        temp = dht_sensor.temperature() # Getting the temperature
        humidity = dht_sensor.humidity() # Getting the humidity
        print('Temperature:', temp)
        print('Humidity:', humidity)

        # Create and send response
        response = html.format(temp, humidity)

        # send HTTP response headers and content to the client
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)

        # close the connection with the client
        cl.close()
    
    except OSError as e:
        # handle connection errors by closing the connection and printing an error message
        cl.close()
        print('connection closed')
