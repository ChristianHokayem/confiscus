from flask import Flask, render_template, request
from random import choice
import RPi.GPIO as GPIO

app = Flask(__name__)

frequency = 10
duty_cycle = 20
pins = [5, 15, 11]

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pins, GPIO.OUT)

@app.route('/')
def index_page():
    return render_template('home.html')

@app.route('/tickle')
def slider_page(methods=["GET", "POST"]):
    data = {
      'title' : 'Confiscus',
      'frequency': frequency,
      'duty_cycle' : duty_cycle
    }
    print("**"*30)
    #freq_value = request.form["freq_value"]
    # print("--- DUTY CYCLE:", dc_value)
    #print("--- FREQUENCY:", freq_value)
    render_template('tickle.html')#, **data)
    if request.method == "POST":
        print("0"*20)
        for i in request.form:
            print("_"*30, i)
    return render_template('tickle.html')#, **data)

@app.route("/control")
@app.route("/control/<pin>")
def control_page(pin=0):
  off_color = 'black'
  on_color = 'yellow'
  colors = [off_color]*3
  
  pin = int(pin)
  if pin in pins:
    GPIO.output(pin, not GPIO.input(pin))
    print("Turning on pin", pin)
    
  for i in range(len(pins)):
    if GPIO.input(pins[i]):
      colors[i] = on_color
      
  print (colors)
  data = {
    'color_led1' : colors[0],
    'color_led2' : colors[1],
    'color_led3' : colors[2],
  }

  return render_template('control.html', **data)

@app.route("/<changePin>/<action>")
def action(changePin, action):
   # Convert the pin from the URL into an integer:
   changePin = int(changePin)
   # Get the device name for the pin being changed:
   deviceName = pins[changePin]['name']
   # If the action part of the URL is "on," execute the code indented below:
   if action == "on":
      # Set the pin high:
      GPIO.output(changePin, GPIO.HIGH)
      # Save the status message to be passed into the template:
      message = "Turned " + deviceName + " on."
   if action == "off":
      GPIO.output(changePin, GPIO.LOW)
      message = "Turned " + deviceName + " off."
   if action == "toggle":
      # Read the pin and set it to whatever it isn't (that is, toggle it):
      GPIO.output(changePin, not GPIO.input(changePin))
      message = "Toggled " + deviceName + "."

   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)

   # Along with the pin dictionary, put the message into the template data dictionary:
   templateData = {
      'message' : message,
      'pins' : pins
   }

   return render_template('main.html', **templateData)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
