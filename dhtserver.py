import time
import network
import socket
from machine import Pin
import dht

dht_pin = Pin(4, Pin.IN)
dht_sensor = dht.DHT11(dht_pin)

ssid = 'guru'
password = 'guru1234'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)


# Wait for connect or fail
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)
    
# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('Connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )
    
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
addr = socket.getaddrinfo('0.0.0.0',45000)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('listening on', addr)

# Listen for connections, serve client
while True:
    try:       
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)
        print("request:")
        print(request)
        request = str(request)

        temp = None
        humidity = None
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
        print('Temperature:', temp)
        print('Humidity:', humidity)

        # Create and send response
        response = html.format(temp, humidity)
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
        
    except OSError as e:
        cl.close()
        print('connection closed')
