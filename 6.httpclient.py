import socket

# Connect to the web server and request temperature and humidity readings
addr = ('192.168.231.57', 8000)
s = socket.socket()
s.connect(addr)
request = b'GET / HTTP/1.1\r\nHost: ' + bytes(addr[0], 'utf8') + b'\r\n\r\n'
s.send(request)

# Receive and decode the server response
response = s.recv(1024).decode('utf8')

# Extract the temperature and humidity readings from the response
temp_start = response.find('Temperature: ') + len('Temperature: ')
temp_end = response.find(' C<br>')
temp = response[temp_start:temp_end]

hum_start = response.find('Humidity: ') + len('Humidity: ')
hum_end = response.find(' %</p>')
hum = response[hum_start:hum_end]

# Print the temperature and humidity readings
print('Temperature:', temp)
print('Humidity:', hum)

# Close the socket
s.close()
