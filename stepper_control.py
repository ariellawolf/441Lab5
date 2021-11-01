#!/usr/bin/python37all
import cgi
import json
import cgitb
cgitb.enable()

action = cgi.FieldStorage() #retrieve button submission

if ("angle" in action):
  selectedAngle = action.getvalue("slider1")
  with open('stepper-angle.txt','w') as f:
    f.write(str(selectedAngle))
elif ("zero" in action):
  with open('stepper-angle.txt','w') as f:
    f.write("0")

print("Content-type: text/html\n\n")
print('<html>")
print('<form action="/cgi-bin/range.py" method="POST">')
print('Select angle (degrees):<br>')
print('<input type="range" name="slider1" min ="0" max="360" value ="180"/><br>')
print('<input type="submit" name= "angle" value="Submit Angle">')
print('<input type="submit" name="zero" value="Zero the Motor">')
print('</form>')
print('Angle selected = %s' % angle)
print('</html>')