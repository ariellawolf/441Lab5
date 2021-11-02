import RPi.GPIO as GPIO
import json
from stepper import Stepper

GPIO.setmode(GPIO.BCM)

pins = [23,24,16,20] # controller inputs: in1, in2, in3, in4
for pin in pins:
  GPIO.setup(pin, GPIO.OUT, initial=0)

photoResistorPin= 26
GPIO.setup(photoResistorPin, GPIO.IN) 
with open('/usr/lib/cgi-bin/stepper-angle.txt','r') as f:
  previous_angle=180

while True:
  with open('/usr/lib/cgi-bin/stepper-angle.txt','r') as f:
    angleRead= json.load(f)
  print(angleRead)  
  action=180
  #action = int(angleRead['slider1'])
  MotorInput= Stepper(action, previous_angle)
  if action== 0:
    MotorInput.zero()
    MotorInput.delay
    previous_angle= 0
  else:
    print("motor turning")
    MotorInput.goAngle()
    previous_angle= action
 