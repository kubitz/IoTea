import paho.mqtt.client as mqtt
import json
import time

class MQTT_RECEIVER():
    def __init__(self, verbose = 0): 
        self.client = mqtt.Client()
        self.client.tls_set(ca_certs="mosquitto.org.crt",certfile="client.crt",keyfile="client.key",tls_version=ssl.PROTOCOL_TLSv1_2)
        self.client.connect("test.mosquitto.org", port=8884)
        self.client.on_message = self.on_message
        self.verbose = verbose
        self.user = None
    def on_message(self,client, userdata, message):
        if self.verbose: 
            print("Received message:{} on topic{}".format(message.payload, message.topic))
        data = json.loads(message.payload)
        self.user = data.get('user')
        
    def get_username(self): 
        self.client.subscribe("IC.embedded/IoTea/user/#")
        time.sleep(0.25)
        for iteration in range(3):
            self.client.loop()
        self.client.unsubscribe("IC.embedded/IoTea/user/#")
        return self.user