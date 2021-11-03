#!/usr/bin/python37all
import cgi
import json

action = cgi.FieldStorage() #retrieve button submission
selectedAngle=180

if ("angle" in action):
  selectedAngle = action.getvalue('slider1')
  data= {"NewAngle":selectedAngle}
elif ("zero" in action):
  selectedAngle = 0
  data= {"NewAngle":selectedAngle}

with open('/usr/lib/cgi-bin/stepper-angle.txt','w') as f:
  json.dump(data,f)

print("Content-type: text/html\n\n")
print('<html>')
print('<form action="/cgi-bin/stepper_control.py" method="POST">')
print('Select angle (degrees):<br>')
print('<input type="range" name="slider1" min ="0" max="360"/><br>')
print('<input type="submit" name= "angle" value="Submit Angle">')
print('<input type="submit" name="zero" value="Zero the Motor">')
print('</form>')
print('Angle selected = %s' % selectedAngle)
print(action)
print('</html>')