# IoTea Source code

**Embedded Folder** contains the code for the Pi

**Frontend Folder** contains the codef for the computer (Web app)

## Embedded Folder
This is a python virtual environment and will be run on the pi. This was coded on a Pi zero using Rasbian. 

The following functions are implemented in this code: 
* Recording voice using a USB microphone
* Recording temperature of probe via OneWire protocol
* Sending the temperature data to the computer via MQTT
* Making API request to Google Cloud text-to-speech API
* Locally run sentiment analysis on the output of Google API
* Use Twitter API to send tweet to @kubitz19 (this can change depending on API key provided)

All the certification files, and API keys have been removed for security reasons. They need to be re-generated to run this code. 
See instructions in Embedded readme

## Frontend Folder

## Generating MQTT encrypted keys
All the MQTT encrypted keys have not been uploaded for security reasons. 
You can generate them yourself by following instructions [here](http://www.steves-internet-guide.com/creating-and-using-client-certificates-with-mqtt-and-mosquitto/).

The same key and .crt files need to be copied to both the Pi and the computer. 
