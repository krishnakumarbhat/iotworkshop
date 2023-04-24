import network

# Set the SSID and password for your Wi-Fi network
ssid = 'your_network_ssid'
password = 'your_network_password'

# Connect to Wi-Fi network
def connect():
    global ssid, password
    station = network.WLAN(network.STA_IF)
    station.active(True)
    if not station.isconnected():
        print('Connecting to network...')
        station.connect(ssid, password)
        while not station.isconnected():
            pass
    print('Network config:', station.ifconfig())

# Call the connect function to initiate the Wi-Fi connection
connect()

