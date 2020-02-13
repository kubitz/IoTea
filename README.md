# IoTea Source code

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
