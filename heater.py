'''
Import the library used to control the steering gear
'''
import Adafruit_PCA9685
import time
from flask import Flask, render_template, request

app = Flask(__name__)
'''
Instantiate the steering gear control object
'''
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)

onValue = 500
offValue = 100

'''
Define the port number of the servo you want to control
'''
servoNum = 15

'''
This is the initial position and the variable used to store the end point of the last movement of the servo
'''
lastPos = 300

'''
Enter a new position in the parameter of this function, the rudder will move smoothly from lastPos to newPosInput
'''
def smoothServo(newPosInput):
	'''
	Declare lastPos as a global variable
	'''
	global lastPos

	'''
	Calculate the difference between lastPos and newPosInput
	'''
	errorPos = newPosInput - lastPos

	'''
	Control the servo to move from lastPos to newPosInput little by little
	'''
	for i in range(0, abs(errorPos)):
		nowPos = int(lastPos + errorPos*i/abs(errorPos))
		pwm.set_pwm(servoNum, 0, nowPos)
		time.sleep(0.01)

	'''
	Update lastPos as the starting point of the next exercise
	'''
	lastPos = newPosInput
	pwm.set_pwm(servoNum, 0, lastPos)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/<deviceName>/")

def action(deviceName):
    if deviceName == 'on':      
        inputValue = onValue
    if deviceName == 'off':
        inputValue = offValue
        smoothServo(inputValue)
        return render_template('index.html')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=2500, debug=True)