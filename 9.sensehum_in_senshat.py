from sense_hat import SenseHat
sense= SenseHat () 
sense.clear()

hum = sense.get_humidity()
temp =sense.get_temperature()

temperature = round(temp,1)
humidity = round(hum,1)

print(temperature)
print(humidity)

sense.show_message('temperature: {str(temp)} humidity: {str(humidity)}')
