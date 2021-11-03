import time
import RPi.GPIO as GPIO

import smbus

class ADC:

  def __init__(self,address):
    self.bus = smbus.SMBus(1)
    self.address = address

  def read(self,chn): #channel
      try:
          self.bus.write_byte(self.address, 0x40 | chn)  # 01000000
          self.bus.read_byte(self.address) # dummy read to start conversion
      except Exception as e:
          print ("Address: %s \n%s" % (self.address,e))
      return self.bus.read_byte(self.address)

  def write(self,val):
      try:
          self.bus.write_byte_data(self.address, 0x40, int(val))
      except Exception as e:
          print ("Error: Device address: 0x%2X \n%s" % (self.address,e))

class Stepper:
  GPIO.setmode(GPIO.BCM)
  sequence = [ [1,0,0,0],[1,1,0,0],[0,1,0,0],[0,1,1,0],
        [0,0,1,0],[0,0,1,1],[0,0,0,1],[1,0,0,1] ]
  pins = [23,24,16,20] # controller inputs: in1, in2, in3, in4
  for pin in pins:
    GPIO.setup(pin, GPIO.OUT, initial=0)

  LED= 26     
  GPIO.setup(LED,GPIO.OUT, initial=0)

  def __init__(self, angle, previous_angle, address):
    self.state= 0 # current position in stater sequence
    self.cur_angle = previous_angle
    self.new_angle= angle
    self.steps= self.angleToHalfSteps()
    self.myADC=ADC(address)

  def angleToHalfSteps(self): #takes difference in angle input and converts to half steps
    if (self.new_angle>270) and (self.cur_angle<90):
      self.angledif= 360-self.new_angle+self.cur_angle
      return self.angledif/360*512*8
    elif (self.new_angle<00) and (self.cur_angle<270):
      self.angledif= 360-self.cur_angle+self.new_angle
      return self.angledif/360*512*8
    else:
      return (self.new_angle-self.cur_angle)/360*512*8



    

  def delay_us(self,tus): # use microseconds to improve time resolution
    endTime = time.time() + float(tus)/ float(1E6)
    while time.time() < endTime:
      pass

  def decideDirection(self): #checks which direction is fastest
    if (0 < (self.new_angle - self.cur_angle) < 180):
      self.dir= -1 #cw
    elif ((self.new_angle - self.cur_angle) > 180):
      if (self.new_angle>270) and (self.cur_angle<90):
        self.dir= 1 #ccw
    elif(-180<(self.new_angle-self.cur_angle)<0):
      self.dir= 1 #ccw-- this works
    elif((self.new_angle - self.cur_angle) < -180):
      if (self.new_angle<90) and (self.cur_angle>270):
          self.dir= -1 #cw
    else:
      self.dir= 1 #ccw

  def halfstep(self): #run through different pins to set states
    # dir = +/- 1 (ccw/ cw)
    self.decideDirection()
    self.state = self.state + self.dir
    if self.state > 7: self.state = 0
    elif self.state < 0: self.state = 7
    for pin in range(4):    # 4 pins that need to be energized
        GPIO.output(self.pins[pin], self.sequence[self.state][pin])
    self.delay_us(1000)

  def goAngle(self): 
    # move the actuation sequence a given number of half steps
    print("doing goAngle")
    print("self.new_angle=",self.new_angle)
    print("self.cur_angle=",self.cur_angle)
    number_halfSteps= int(self.angleToHalfSteps())
    for step in range(number_halfSteps):
      self.halfstep()
    time.sleep(1)
    
  
  def zero(self):
    # move the actuation sequence until photoresistor reads low
    self.input=self.myADC.read(0)
    print(self.input)
    while self.input<180:
      self.halfstep()
      GPIO.output(Stepper.LED,1)
      self.input= self.myADC.read(0)
      print(self.input)
    GPIO.output(Stepper.LED,0)
    

