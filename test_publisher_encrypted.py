import paho.mqtt.client as mqtt
import ssl 
client = mqtt.Client()
client.tls_set(ca_certs="mosquitto.org.crt", certfile="client.crt",keyfile="client.key",tls_version=ssl.PROTOCOL_TLSv1_2)
client.connect("test.mosquitto.org", port=8884)
client.publish("IC.embedded/IoTea/test", "Hello Luccas")

client.publish("IC.embedded/IoTea/test", "The Car Is On Fire. The Government Is Corrupt.")
