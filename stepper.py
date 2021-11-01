import time
import RPi.GPIO as GPIO

class Stepper:
  GPIO.setmode(GPIO.BCM)
  sequence = [ [1,0,0,0],[1,1,0,0],[0,1,0,0],[0,1,1,0],
        [0,0,1,0],[0,0,1,1],[0,0,0,1],[1,0,0,1] ]
  pins = [23,24,16,20] # controller inputs: in1, in2, in3, in4
  for pin in pins:
    GPIO.setup(pin, GPIO.OUT, initial=0)

  photoResistorPin= 6     

  def __init__(self, angle):
    self.state= 0 # current position in stater sequence
    self.cur_angle = angle
    self.steps= self.angleToHalfSteps(angle)
    self.tus= 1/self.speed*60*10^6 #converts RPM to usec/rev

  def angleToHalfSteps(self): #takes difference in angle input and converts to half steps
    return (self.new_angle-self.cur_angle)/360*512*8

  def delay_us(self,tus): # use microseconds to improve time resolution
    endTime = time.time() + float(tus)/ float(1E6)
    while time.time() < endTime:
      pass

  def decideDirection(self): #checks which direction is fastest
    if (0 < (self.new_angle - self.cur_angle) < 180):
      self.dir= 1
    elif (180 > (self.new_angle - self.cur_angle) > 0):
      self.dir= 1
    else:
      self.dir= -1

  def halfstep(self): #run through different pins to set states
    # dir = +/- 1 (ccw/ cw)
    self.decideDirection()
    self.state += self.dir
    if self.state > 7: self.state = 0
    elif self.state < 0: self.state = 7
    for pin in range(4):    # 4 pins that need to be energized
        GPIO.output(self.pins[pin], self.sequence[self.state][pin])
    self.delay_us(1000)

  def goAngle(self): 
    # move the actuation sequence a given number of half steps
    self.halfSteps= self.angleToHalfSteps()
    for step in self.halfSteps:
      self.halfstep()
  
  def zero(self):
    # move the actuation sequence until photoresistor reads low
    self.new_angle=0
    self.input= GPIO.input(self.photoResistorPin)
    while self.input>0:
      self.halfstep()
      self.input= GPIO.input(self.photoResistorPin)
    

