import RPi.GPIO as GPIO
import stepper.py

GPIO.setmode(GPIO.BCM)

pins = [23,24,16,20] # controller inputs: in1, in2, in3, in4
for pin in pins:
  GPIO.setup(pin, GPIO.OUT, initial=0)

photoResistorPin= 26
GPIO.setup(photoResistorPin, GPIO.IN) 

with open("stepper-angle.txt",'r') as f:
  action = int(f.read())

MotorInput= stepper.Stepper(action)
if ("0" in action):
  MotorInput.zero()
  MotorInput.delay
else:
  MotorInput.GoAngle()
  