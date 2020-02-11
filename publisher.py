import paho.mqtt.client as mqtt

class MQTT():

    def __init__(self):
        self.client = mqtt.Client()


    def publish(self, value):
        self.client.connect("test.mosquitto.org", port=1883)
        self.client.publish("IC.embedded/IoTea/test", str(value))

