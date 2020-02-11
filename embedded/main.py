from RecordMic import Microphone
from TwitterBot import TwitterBot
from SpeechProcessing import SpeechToText
from Temp import TemperatureSensor
import paho.mqtt.client as mqtt
import ssl 
import time
import json

class DataPacket: 
    def __init__(self): 
        self.temp_data = dict()
        self.sentiment_data = dict()
        self.start_time = time.time()

    def add_temp_data(self, temp_data): 
        """ Adds a temperature data point to class instance with a timestamp
        """
        timestamp = self._get_timestamp()
        self.temp_data.update({timestamp: temp_data})       

    def add_sentiment_data(self, sentiment_data): 
        """ Adds a sentiment data point to class instance with a timestamp
        """
        timestamp = self._get_timestamp() 
        self.sentiment_data.update({timestamp: sentiment_data})       

    def format_mqtt_message(self)
        """ Formats data in json file to be sent via MQTT
        """
        data_packet = {'temperature':self.temp_data,
                        'sentiment':self.sentiment_data
                        }

        json_packet = json.dumps(data_packet)
        return json_packet

    def _get_timestamp(self): 
        """ Return timestamp since DataPacket instance was initialized
        """
        elapsed_time = time.time() - self.start_time
        timestamp = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
        return timestamp

if __name__ == "__main__":
    microphone = Microphone()
    twitter_bot = TwitterBot()
    speech_to_text = SpeechToText()
    thermometer = TemperatureSensor()
    data_packet  = DataPacket()
    client = mqtt.Client()


    print("Initialisation done!!!")
    
    while True: 
        if microphone.is_talking(): 
            print("Volume detected!")
            microphone.record_to_file(15)
            conversation  = speech_to_text.get_text((microphone.record_counter-1)%5)
            if conversation is not None: 
                try: 
                    sentiments = speech_to_text.get_sentiment(conversation)
                    twitter_bot.send_tweet(sentiments[0][0])
                    average_sentiment = speech_to_text.get_average_sentiment(sentiments)
                    data_packet.add_sentiment_data(average_sentiment)

                except: 
                    print("ERROR: Could not process the audio file \n The file probably did not contain speech.")

        temperature = thermometer.get_temp()
        data_packet.add_temp_data(temperature)