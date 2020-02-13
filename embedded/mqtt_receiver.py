""" This file runs in parallel to the main
    It receives any message sent from the broker
    It saves it in a text file
"""
import paho.mqtt.client as mqtt
import ssl 
import json
import time
def on_message(client, userdata, message):
    print("Received message:{} on topic{}".format(message.payload, message.topic))
    data = json.loads(message.payload)
    print(data)
    user = data.get('user')
    print(user)

    with open("user_data.txt", "w") as file:
        file.write(user)


client = mqtt.Client()
client.tls_set(ca_certs="mosquitto.org.crt",certfile="client.crt",keyfile="client.key",tls_version=ssl.PROTOCOL_TLSv1_2)
client.connect("test.mosquitto.org", port=8884)
client.on_message = on_message

while True:
    print("Entered sleep!")
    time.sleep(1)
    print("Came out of sleep!")
    
    client.subscribe("IC.embedded/IoTea/user/#")
    time.sleep(0.25)
    for iteration in range(3):
        client.loop()
    client.unsubscribe("IC.embedded/IoTea/user/#")