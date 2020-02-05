import paho.mqtt.client as mqtt
import Temp006
#import ssl 
client = mqtt.Client()
#client.tls_set(ca_certs="mosquitto.org.crt",
#certfile="client.crt",keyfile="client.key",tls_version=ssl.PROTOCOL_TLSv1_2)
client.connect("test.mosquitto.org", port=1883)

mytemp = Temp()
mytemp.begin()
temp = mytemp.log_temp()
client.publish(temp, "Hello Luccas")
