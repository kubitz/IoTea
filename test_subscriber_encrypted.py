import paho.mqtt.client as mqtt
import ssl 
def on_message(client, userdata, message):
    print("Received message:{} on topic{}".format(message.payload, message.topic))
client = mqtt.Client()
client.tls_set(ca_certs="mosquitto.org.crt",certfile="client.crt",keyfile="client.key",tls_version=ssl.PROTOCOL_TLSv1_2)
client.connect("test.mosquitto.org", port=8884)
client.subscribe("IC.embedded/IoTea/test/#")
client.on_message = on_message

while 1 == 1:
    client.loop()




