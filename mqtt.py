import paho.mqtt.client as mqtt
# This is test 
client = mqtt.Client()
client.connect("test.mosquitto.org", port=1883)
client.publish("IC.embedded/IoTea/test", "hello")
mqtt.error_string(MSG_INFO.rc)
