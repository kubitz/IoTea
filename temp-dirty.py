    from w1thermsensor import W1ThermSensor
    import paho.mqtt.client as mqtt
    import threading
    
    
    sensor = W1ThermSensor()
    client = mqtt.Client()
    
    def main():
        temp = sensor.get_temperature()
        client.connect("test.mosquitto.org", port=1883)
        client.publish("IC.embedded/IoTea/test", str(temp))
        threading.Timer(3, main).start()