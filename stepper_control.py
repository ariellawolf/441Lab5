#!/usr/bin/python37all
import cgi
import json

action = cgi.FieldStorage() #retrieve button submission
selectedAngle=180
if ("angle" in action):
  selectedAngle = int(action.getvalue('slider1'))
  dataDump= {"NewAngle":selectedAngle}
  with open('stepper_control.py','w') as f:
    json.dump(dataDump,f)
elif ("zero" in action):
  selectedAngle = 0
  dataDump= {"NewAngle":0}
  with open('stepper_control.py','w') as f:
    json.dump(dataDump,f)

print("Content-type: text/html\n\n")
print('<html>')
print('<form action="/cgi-bin/stepper_control.py" method="POST">')
print('Select angle (degrees):<br>')
print('<input type="range" name="slider1" min ="0" max="360" value ="180"/><br>')
print('<input type="submit" name= "angle" value="Submit Angle">')
print('<input type="submit" name="zero" value="Zero the Motor">')
print('</form>')
print('Angle selected = %s' % selectedAngle)
print(action)
print('</html>')