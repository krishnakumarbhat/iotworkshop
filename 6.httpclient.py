import network
import socket

# Set up Wi-Fi connection
ssid = 'abc'
password = 'asdf1234'
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# Wait for Wi-Fi connection
while not wlan.isconnected():
    pass

# Fetch temperature and humidity data from server
url = 'http://192.168.136.75/'
_, _, host, path = url.split('/', 3)
addr = socket.getaddrinfo(host, 45000)[0][-1]
s = socket.socket()
s.connect(addr)
s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))

data = ''
while True:
    chunk = s.recv(128)
    if not chunk:
        break
    data += str(chunk, 'utf8')

# Extract temperature and humidity values from data
temp_start = data.find('Temperature: ') + len('Temperature: ')
temp_end = data.find(' C')
temp = float(data[temp_start:temp_end])
hum_start = data.find('Humidity: ') + len('Humidity: ')
hum_end = data.find(' %')
hum = int(data[hum_start:hum_end])

# Print temperature and humidity values
print('Temperature:', temp, 'C')
print('Humidity:', hum, '%')
