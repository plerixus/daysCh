import time
import RPi.GPIO as GPIO
import datetime
import dht11


GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)
sensor = dht11.DHT11(pin=4)
sleepTime = 300
pinList = [14, 15, 18, 17]
log_file = "results24h.txt"

def local_log(file_name, time_stamp, temperature, humidity, lamp_state):
	''' logs data on a local file '''
	log_file = open(file_name,"a")
	log_file.write("\nLast input:\t" + str(time_stamp))
	log_file.write("\nTemperature:\t" + str(temperature))
	log_file.write("\nHumidity:\t" + str(humidity))
	log_file.write("\nLamp is:\t" + str(lamp_state) + "\n")
	log_file.write("-" * 48)
	log_file.close()

for i in pinList:
	GPIO.setup(i, GPIO.OUT)
	GPIO.output(i, GPIO.LOW)

try:
    while True:
		now = datetime.datetime.now().hour
		result = sensor.read()
		timeOffset = 0
		while (result.is_valid() == False):
			result = sensor.read()
			timeOffset = timeOffset + 1
			time.sleep(1)

		if (now > 12):
			GPIO.output(14, GPIO.HIGH)
			lamp_is = "ON"

		else:
			lamp_is = "OFF"

		local_log(
			log_file,
			datetime.datetime.now(),
			result.temperature,
			result.humidity,
			lamp_is
			)


		time.sleep(sleepTime-timeOffset)

    GPIO.cleanup()

except KeyboardInterrupt:
	print("Keyboard quit")
	GPIO.cleanup()
