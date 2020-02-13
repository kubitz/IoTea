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
* Use Twitter API to send tweet to [@kubitz19](https://twitter.com/Kubitz19) (this can change depending on API key provided)

All the certification files, and API keys have been removed for security reasons. They need to be re-generated to run this code. 
See instructions in Embedded readme

### Generating Google API keys
For the speech-to-text function to work, a file named "apikey.json" needs to be added in the origin/master/embedded folder. 
This file can be downloaded from [Google Cloud's platform](https://console.cloud.google.com/) after activating the API and setting-up payement details (300$ of free credit at subscription). 

You can find more details on setting-up your Google Cloud API key [here](https://cloud.google.com/iam/docs/creating-managing-service-account-keys).

### Set-up Twitter credentials
For TwitterBot.py to work, a Twitter developper account needs to be set-up and credentials need to be added to a twitter_credentials.py file, located in the origin/master/embedded folder.

The file should be formated in the following way: 
~~~~{.python}
ACCESS_TOKEN = "insert access token here"
ACCESS_TOKEN_SECRET = "insert access token secret here"
CONSUMER_KEY = "insert consumer key here"
CONSUMER_SECRETS = "insert consumer secrets here"
~~~~

For more information on how to get those keys and token, please refer to the offical [twitter developper documentation](https://developer.twitter.com/en/docs/basics/authentication/oauth-1-0a/obtaining-user-access-tokens)

## Computer Side:

### Function:
folder to begin executing the backend: this will generate a data.txt file for communication between the frontend and the backend, and it will process instruction from the raspberry pi. Finally the frontend.py must be launched in order to initiate the local webserver, which will automatically be opened on your local browser.

This code performs the following:
 *Receives data from the raspberry pi through MQTT
 *Processes information to determine time until Tea is cold, wheter the thermometer is heating up, or if the tea is too cold
 *The frontend displays information on your tea
 *Displays the happiness of your current conversation
 *Outputs the tea temperature in graph form

### File Structure:
The main.py receives instructions from the raspberry pi, processess them, and output them on a data.txt file in JSON format. The frontend.py uses the dash library in order to run a local webserver for the user interface. The dash library does not work well with the "threading" library or "paho", which is why the mail files are seperated.

The assets folder stores the CSS data for the layout of the applicatipn.

### Launching the web app:
Before launching the following libraries need to be installed:
*dash
*json
*paho
*threading

Ensure that the .crt and .key files have been generated and are put into the root directory of the folder as instructed in the following section.

Once completed, you must launch the main.py and the frontend.py. The GUI should automatically open with your default browser. 

## Generating MQTT encrypted keys
All the MQTT encrypted keys have not been uploaded for security reasons. 
You can generate them yourself by following instructions [here](http://www.steves-internet-guide.com/creating-and-using-client-certificates-with-mqtt-and-mosquitto/).

The same key and .crt files need to be copied to both the Pi and the computer. 
