from sense_hat import SenseHat
sense= SenseHat () 
sense.clear()
humidity = sense.get_humidity()
print (humidity)


from sense_hat import SenseHat 
sense =SenseHat () 
sense.clear()
ptemp = sense.get_temperature_from_pressure()
htemp =sense.get_temperature_from_humidity()
temp = (ptemp+htemp)/2

print (ptemp)
print (htemp)
print(temp)
sense.show_message(str(temp) + str(humidity))
