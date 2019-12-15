import time
import RPi.GPIO as GPIO
import Adafruit_DHT
import sshtunnel
import mysql.connector
import myDetails


GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)
sensor=Adafruit_DHT.DHT11
sensor_pin=4
sleepTime = 300
pinList = [14, 15, 18, 17]
log_file = "results24h.txt"
sshtunnel.SSH_TIMEOUT = 5.0
sshtunnel.TUNNEL_TIMEOUT = 5.0
add_to_log = ("INSERT INTO Log (H_ID, Temperature_C, Humidity) VALUES (%s, %s, %s)")

def local_log(file_name, time_stamp, temperature, humidity, lamp_state):
	''' logs data on a local file, only used when need to test on spot '''
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

with sshtunnel.SSHTunnelForwarder(
	('ssh.pythonanywhere.com'),
	ssh_username=myDetails.SSH_USERNAME, ssh_password=myDetails.SSH_PASSWORD,
	remote_bind_address=(myDetails.MYSQL_BIND, 3306)
	) as tunnel:

	try:
		while True:
			humidity, temperature = Adafruit_DHT.read_retry(sensor, sensor_pin)
			timeOffset = 0
			while (humidity is None or temperature is None):
				humidity, temperature = Adafruit_DHT.read_retry(sensor, sensor_pin)
				timeOffset = timeOffset + 1
				time.sleep(1)
			connection = mysql.connector.connect(
				user=myDetails.SSH_USERNAME, password=myDetails.MYSQL_PASSWORD,
				host='127.0.0.1', port=tunnel.local_bind_port,
				database=myDetails.MYSQL_DATABASE)

			cursor = connection.cursor()
			log_values = ("1", temperature , humidity)
			cursor.execute(add_to_log, log_values)
			connection.commit()
			connection.close()
			if(timeOffset>=299):
				timeOffset = 290
			time.sleep(sleepTime-timeOffset)

	except KeyboardInterrupt:
		print("Keyboard quit")
		GPIO.cleanup()
		cursor.close()
		connection.close()
