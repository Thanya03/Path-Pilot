import RPi.GPIO as GPIO
from time import sleep
import requests

GPIO.setwarnings(False)

in1 = 17
in2 = 27
en_a = 4

in3 = 26
in4 = 6
en_b = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(en_a, GPIO.OUT)

GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
GPIO.setup(en_b, GPIO.OUT)

p = GPIO.PWM(en_a, 1000)  # Set PWM frequency
p.start(0)  # Start with 0 duty cycle

q = GPIO.PWM(en_b, 100)
q.start(0)

# Define your ThingSpeak channel ID and read API key
channel_id = '2316050'
read_api_key = 'MTXA3CNFWRB5X60R'

# URL for reading the latest entry from the channel
url = f'https://api.thingspeak.com/channels/{channel_id}/feeds/last.json?api_key={read_api_key}'

try:
    while True:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'field1' in data:
                integer_value = int(data['field1'])
                print(f"Speed is: {integer_value}")
                p.ChangeDutyCycle(integer_value)
                q.ChangeDutyCycle(integer_value)
                GPIO.output(in1, GPIO.HIGH)
                GPIO.output(in2, GPIO.LOW)
                GPIO.output(in3, GPIO.HIGH)
                GPIO.output(in4, GPIO.LOW)
                sleep(5)
            else:
                print(f"The key does not exist in the dictionary.")

except KeyboardInterrupt:
    # Reset GPIO settings
    GPIO.cleanup()
    print("GPIO Clean up")

