import RPi.GPIO as GPIO
import time

servoPIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

servo = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
servo.start(0) # Initialization
print("Waiting for 1 second")
time.sleep(1)
duty=2 # 0 degrees
servo.ChangeDutyCycle(duty)

'''try:
  while True:
    angle = input("Enter angle: ")
    if angle == 'q':
      servo.stop()
      GPIO.cleanup()
      break
    elif angle == 'h': # Hold position
      dutyCycle = 0
    else:
      angle = float(angle)
      dutyCycle = (angle/22.5)+2
    servo.ChangeDutyCycle(dutyCycle)
except KeyboardInterrupt:
  servo.stop()
  GPIO.cleanup()'''

for i in range(0,180):
  angle = float(i)
  dutyCycle = (angle/22.5)+2
  servo.ChangeDutyCycle(dutyCycle)

time.sleep(2)

for i in range(0,180):
  angle = float(180-i)
  dutyCycle = (angle/22.5)+2
  servo.ChangeDutyCycle(dutyCycle)
  
servo.stop()
GPIO.cleanup()