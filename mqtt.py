import paho.mqtt.client as mqtt
import ssl 
client.tls_set(ca_certs="mosquitto.org.crt",
certfile="client.crt",keyfile="client.key",tls_version=ssl.PROTOCOL_
TLSv1_2)client = mqtt.Client()
client.connect("test.mosquitto.org", port=8884)
client.publish("IC.embedded/IoTea/test", "hello")
mqtt.error_string(MSG_INFO.rc)
