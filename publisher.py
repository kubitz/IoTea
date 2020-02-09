import paho.mqtt.client as mqtt

class MQTT():

    def __init__(self):
        client = mqtt.Client()


    def publish(self, value):
        client.connect("test.mosquitto.org", port=1883)
        client.publish("IC.embedded/IoTea/test", str(value))

