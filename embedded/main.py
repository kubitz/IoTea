from RecordMic import Microphone
from TwitterBot import TwitterBot
from SpeechProcessing import SpeechToText
from Temp import TemperatureSensor
import paho.mqtt.client as mqtt
import ssl 
from threading import Thread, Event
import time

class SensorRead_threaded(Thread):
    def __init__(self, event, sensor, read_interval = 5, send_interval = 5):
        Thread.__init__(self)
        self.stopped = event
        self.read_interval = read_interval
        self.read_count = 0
        self.data = []
        self.sensor = sensor
    
    def run(self):
        while not self.stopped.wait(self.read_interval):
            temperature = self.sensor.get_temperature()
            self.data.append(temperature)
            self.read_count += 1
            print("reading sensor temperature")
            if self.read_count%self.read_interval is 0: 
                print("Data sent!", self.data)
                self.data = []



if __name__ == "__main__":
    microphone = Microphone()
    twitter_bot = TwitterBot()
    speech_to_text = SpeechToText()
    thermometer = TemperatureSensor()
    
    client = mqtt.Client()

    stop_thread = Event()
    thread_sensor = SensorRead_threaded(stop_thread,thermometer)
    print("Initialisation done!!!")
    
    while True: 
        if microphone.is_talking(): 
            print("Volume detected!")
            microphone.record_to_file(15)
            conversation  = speech_to_text.get_text(microphone.record_counter%5)
            sentiments = speech_to_text.get_sentiment(conversation)
            twitter_bot.send_tweet(sentiments)





