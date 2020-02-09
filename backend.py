import paho.mqtt.client as mqtt
import json

def on_message(client, userdata, message):
    #print("Received message:{} on topic{}".format(message.payload, message.topic))
    #print(message.payload)
    temp = float(message.payload)
    data = {}
    data['temp'] = []
    data['temp'].append({
        'Temperature': temp,
    })

    with open('data.txt', 'w') as outfile:
        json.dump(data, outfile)



client = mqtt.Client()
client.connect("test.mosquitto.org", port=1883)
client.subscribe("IC.embedded/IoTea/test/#")
client.on_message = on_message

while 1==1:
    client.loop()

