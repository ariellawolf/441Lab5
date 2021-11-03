import RPi.GPIO as GPIO
import json
from stepper import Stepper

GPIO.setmode(GPIO.BCM)

pins = [23,24,16,20] # controller inputs: in1, in2, in3, in4
for pin in pins:
  GPIO.setup(pin, GPIO.OUT, initial=0)

LED= 26
GPIO.setup(LED, GPIO.OUT) 

previous_angle=180
action=180
MotorInput= Stepper(action, previous_angle,0x48)

while True:
  try:
    with open('/usr/lib/cgi-bin/stepper-angle.txt','r') as f:
      angleRead= json.load(f)
      action= int(angleRead['NewAngle'])
    
    
    if action== 0:
      MotorInput.new_angle=0
      print("motor zeroing")
      MotorInput.zero()
      GPIO.output(LED,0)
      MotorInput.cur_angle= 0
    else:
      print("motor turning")
      MotorInput.new_angle=action
      MotorInput.goAngle()
      MotorInput.cur_angle= action
  except Exception as e:
    print(e)
  
 