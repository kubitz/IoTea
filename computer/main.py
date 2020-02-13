import paho.mqtt.client as mqtt
import ssl
import json
import threading
from TeaProcessing import *

#MIN_TEMP sets the temperature the threshold below which tea is considered cold
MIN_TEMP = 55

first_message_received = False
new_message_received = False

mqtt_input = {}

client = mqtt.Client()
sentiment_data = []

tea_data = {
    'time': [],
    'temp': []
}

def get_state(current_temp):
    """
    Uses the current temp to determine if the sensor is heating up, the tea is too cold, or the tea is cooling down
    inputs: The current temperature
    output: the state, a variable used by the frontend and further calculations
    """

    global tea_data
    state = ''
    print(tea_data['temp'])
    if len(tea_data['temp']) >= 2:
        rising = is_sensor_ready(tea_data['temp'])
        if rising:
            state = 'rising'
        elif current_temp > MIN_TEMP:
            state = 'ready'
        else:
            state = 'cold'
    else:
        state = 'nodata'

    return state

def get_sentiment():
    """
    Takes the list of sentiments received from pi - uses the last one and converts it from -1,1 to 0,10
     inptuts: global variable sentiment data received from Pi
     outputs: last sentiment in usable range
    """

    global sentiment_data
    if len(sentiment_data) != 0:
        current_sentiment = 5 * sentiment_data[-1] + 5
    else:
        current_sentiment = 5
    return current_sentiment

def get_current_temp():
    """
    Returns the current_temp as last variable from list
    inputs: global variable tea_data
    output: current temp
    """
    global tea_data
    current_temp = 0
    if len(tea_data['temp']) != 0:
        current_temp = tea_data['temp'][-1]
    return current_temp

def update_tea_data(new_times, new_temps):
    """
    appends the new time, temp data to the global variable which stores all history.
    this function is only called whenever a new message is received
    inputs: local variable new_times, new_temps
    outputs: gloval variable tea_data
    """

    global tea_data
    tea_data['time'] += new_times
    tea_data['temp'] += new_temps

def get_time_to_cool(current_temp, state):
    """
    returns time until cool but only if tea is cooling down
    input: current temperature
    output: the temperature at which tea is considered cold
    """
    if state == 'ready':
        time = predict_teacup_temp(current_temp, MIN_TEMP)//60
    else:
        time = 0
    return time

def update_sentiment(new_sentiment):
    """
    Appends new sentiment data to list of all previous sentiments
    input: new_sentiment data
    output: global sentiment data
    """
    global sentiment_data
    sentiment_data += new_sentiment

def processing():
    """
    Main loop that executes every 3 seconds on seperate thread.
    It processess incoming data from the recieved MQTT, and outputs new parameters as JSON file
    JSON file is read by frontend in order to display data
    Input: global variables from MQTT thread
    Output: data in JSON file
    """

    #Variables are global and updated every time message is received, processing() does not modify them.
    global mqtt_input
    global new_message_received
    global first_message_received

    display = {}

    #Execute if new MQTT has been received
    if new_message_received:
        new_times = mqtt_input['temperature']['time']
        new_temps = mqtt_input['temperature']['temps']
        new_sentiment = mqtt_input['sentiment']

        #Store new data in global variables tea_data, and sentiment_data
        update_sentiment(new_sentiment)
        update_tea_data(new_times, new_temps)
        new_message_received = False

    #Execute as long MQTT has been received once i.e data exists
    if first_message_received:
        current_temp = get_current_temp()
        state = get_state(current_temp)
        display['time_left'] = get_time_to_cool(current_temp, state)
        display['sentiment'] = get_sentiment()
        display['state'] = state
        display['times'] = tea_data['time']
        display['temps'] = tea_data['temp']
        display['current_temp'] = current_temp

    #Execute if no MQTT has been received
    else:
        display['state'] = 'nodata'

    with open('data.txt', 'w') as f:
        json.dump(display, f, ensure_ascii=False)

    threading.Timer(3, processing).start()


def on_message(client, userdata, message):
    """
    Receives message and updates mqtt_input, raises first message flag for first message and new_message_flag every message
    inputs: client, userdata, message
    outputs: mqtt_input
    """

    global mqtt_input
    global first_message_received
    global new_message_received

    first_message_received = True
    new_message_received = True

    content = message.payload
    mqtt_input = json.loads(content)



def poll_mqtt():
    """
    connects to mqtt and initiates the on_message function
     inputs: client
     outputs: none
    """

    try:
        client.tls_set(ca_certs="mosquitto.org.crt", certfile="client.crt", keyfile="client.key", tls_version=ssl.PROTOCOL_TLSv1_2)
    except:
        print("you do not have the required files")
    try:
        client.connect("test.mosquitto.org", port=8884)
    except:
        print("unable to connect")
    try:
        client.subscribe("IC.embedded/IoTea/test/#")
    except:
        print("unable to subscribe")
    client.on_message = on_message





if __name__ == '__main__':
    """
    Create data.txt for data transfer between frontend and backend, initiates processing thread, and poll_mqtt()
    """

    # either creates data.txt or replaces it with blank file
    f = open("data.txt", "w+")
    f.write('{"state": "nodata"}')
    f.close()

    #run the front end
    #os.system('python test.py')
    # initiate the main processing loop
    processing()

    poll_mqtt()

    while True:
        client.loop()









