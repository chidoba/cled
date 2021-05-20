FROM balenalib/raspberry-pi-python:3-latest

# Install gcc and build-essential
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y gcc build-essential libjpeg8-dev zlib1g-dev libusb-dev libtiff5 libopenjp2-7

# Install pip dependencies for raspberry pi and ws281x
RUN pip3 install rpi_ws281x adafruit-circuitpython-neopixel RPi.GPIO flask flask-cors python-escpos
RUN python3 -m pip install --force-reinstall adafruit-blinka

# Copy the python script to the workdir
WORKDIR /usr/src/app
COPY cled.py .

# Expose the port of the application
EXPOSE 5000
RUN chmod +x cled.py

CMD [ "python", "./cled.py" ]