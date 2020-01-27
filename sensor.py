from random import randint
import RPi.GPIO as GPIO
import json
import paho.mqtt as mqtt
import time 

class GeigerMeter: 
    def __init__(self, pin_signal = 5, pin_noise = 4): 
        self.pin_signal = pin_signal
        self.pin_noise = pin_noise
        self.radiation_level = self.read_radiation()
        self.uncertainty = 0
        self._cpm = 0
        GPIO.setup(self.pin_signal, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
        GPIO.add_event_detect(self.pin_signal,GPIO.FALLING, callback = self._geiger_pulse_handler, bouncetime = 70)
    
    def read_radiation(self): 
         self.radiation_level = randint(1, 200)
         self.uncertainty = randint(1,300)
         return self.radiation_level

    def _geiger_pulse_handler(self):
        self._cpm += 1


    def format_data(self): 
        data = {'radiation': self.radiation_level
                ,'uncertainty': self.uncertainty
                    }
        data_json = json.dumps(data)
        return data_json
    
    def __del__(self): 
        print("Sensor Deleted!")
        GPIO.cleanup()

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    sensor = GeigerMeter()
    data = sensor.format_data()
    print(data)
