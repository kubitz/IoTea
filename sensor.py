from random import randint
import json

class GeigerMeter: 
    def __init__(self, pin_signal = 5, pin_noise = 4): 
        self.pin_signal = pin_signal
        self.pin_noise = pin_noise
        self.radiation_level = self.read_radiation()
        self.uncertainty = 0
    
    def read_radiation(self): 
         self.radiation_level = randint(1, 200)
         self.uncertainty = randint(1,300)
         return self.radiation_level


    def format_data(self): 
        data = {'radiation': self.radiation_level
                ,'uncertainty': self.uncertainty
                    }
        data_json = json.dumps(data)
        return data_json


if __name__ == "__main__":
    
    sensor = GeigerMeter()
    data = sensor.format_data()
    print(data)