#!/usr/bin/python3

import board
import neopixel
from escpos.printer import Usb
from flask import Flask
from flask import request
import time
from threading import Thread

# Amount of LEDs that the strip has
LED_COUNT = 200

# Create the neopixel object
pixels = neopixel.NeoPixel(
    board.D18, LED_COUNT, auto_write=False, brightness=0.9)

# Represents an led
class CLed:
    def __init__(self, color, blinking):
        self.color = color
        self.blinking = blinking


# List of all leds that are initialized
cleds = []
for i in range(LED_COUNT):
    cleds.append(CLed((0, 0, 0), False))

# Create a new flask instance that
app = Flask(__name__)

@app.route('/health', methods=['GET'])
# GET endpoint that always responds ok
def health():
    return 'OK', 200

@app.route('/', methods=['POST'])
# POST endpoint that handles updates to the led array
def update():
    # Get the json content that has been sent
    content = request.get_json()
    # Iterate through all leds in the json content
    for led in content:
        # If pin or color of the led is not set, abort with 400
        if 'pin' not in led:
            return 'ERROR', 400
        # Set the default color of the led to black
        if 'color' not in led or len(led['color']) != 3:
            led['color'] = [0, 0, 0]
        # Set the blinking default to false
        if 'blinking' not in led:
            led['blinking'] = False
        # Set the state of the new led
        color = led['color']
        cleds[led['pin']] = CLed(
            (color[0], color[1], color[2]), led['blinking'])
    # Return ok because the state was updated successfully
    return 'OK', 200

@app.route('/print', methods=['POST'])
# POST endpoint that prints received input on the thermalprinter
def print():
    # Get the text content that has been sent
    content = request.data
    # Establish connection to the usb device
    p = Usb(0x0416, 0x5011, out_ep=3)
    p.text(content.decode("utf-8"))
    p.cut()
    p.close()
    # Return a success message because everything worked correctly
    return 'OK', 200

class LedLoop(Thread):
    # Loop that runs every second and turns on the appropriate leds
    def run(self):
        blinkingState = False
        # Loop
        while True:
            # Invert the blinking state for every run
            blinkingState = not blinkingState
            # Iterate through all leds and check whether they should be on
            for i in range(LED_COUNT):
                cled = cleds[i]
                # Check whether the led should be on and turn them on with the set color
                if (not cled.blinking or blinkingState):
                    pixels[i] = cled.color
                else:
                    pixels[i] = (0, 0, 0)
            # Show the new colors and sleep for half a second
            pixels.show()
            time.sleep(0.5)


# Main method of this application
if __name__ == '__main__':
    # Start the led_loop in the background
    LedLoop().start()
    # Run the flask app server
    app.run(host="0.0.0.0")