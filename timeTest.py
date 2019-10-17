import time
import RPi.GPIO as GPIO
import datetime
import dht11


GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)
sensor = dht11.DHT11(pin=4)
sleepTime = 300
pinList = [14, 15, 18, 17]

for i in pinList:
	GPIO.setup(i, GPIO.OUT)
	GPIO.output(i, GPIO.LOW)

try:
    while True:
		now = datetime.datetime.now().hour
		log = open("results24h.txt","a")
		result = sensor.read()
		timeOffset = 0
		while (result.is_valid() ==False):
			result = sensor.read()
			timeOffset = timeOffset + 1
			time.sleep(1)
		log.write("\nLast input:\t" + str(datetime.datetime.now()))
		log.write("\nTemperature:\t" + str(result.temperature))
		log.write("\nHumidity:\t" + str(result.humidity))

		if (now > 12):
			GPIO.output(14, GPIO.HIGH)
			now=datetime.datetime.now().hour
			log.write("\nLamp is:\tON\n")

		else:
			log.write("\nLamp is:\tOFF\n")

		log.write("-"*48)
		log.close()

		time.sleep(sleepTime-timeOffset)

    GPIO.cleanup()

except KeyboardInterrupt:
	print("Keyboard quit")
	GPIO.cleanup()
