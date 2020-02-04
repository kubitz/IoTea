import Adafruit_GPIO.I2C as I2C
from time import gmtime, strftime
import json
import math


pin_address = 0x40  #adress location for RPi I2C
config_reg = 0x02    #register address for configuration data
object_vol_reg = 0x0
ambient_reg = 0x01
config_val = 0x79  #Device in active mode, output low (I think), 16 samples

B0   = -0.0000294
B1   = -0.00000057
B2   = 0.00000000463
C2   = 13.4
TREF = 298.15
A2   = -0.00001678
A1   = 0.00175
S0   = 6.4  # * 10^-14

class Temp():

    def __init__(self):
        self.temperature = 0
        self.time = 0
        try:
            self.sensor = I2C.get_i2c_device(pin_address)
        except:
            print("Error: Connect I2C device")

    def begin(self):
        self.sensor.write16(config_reg, config_val)

    def calc_temp(self, die_temp, obj_vol):      
        die_temp_ref = die_temp - TREF
        S = 1.0 + A1*die_temp_ref + A2*math.pow(die_temp_ref, 2.0)
        S *= S0
        S /= 10000000.0
        S /= 10000000.0
        Vos = B0 + B1*die_temp_ref + B2*math.pow(die_temp_ref, 2.0)
        fobj_vol = (obj_vol - Vos) + C2*math.pow((obj_vol - Vos), 2.0)
        obj_temp = math.sqrt(math.sqrt(math.pow(die_temp, 4.0) + (fobj_vol/S)))
        return obj_temp - 273.15

    def read_die_temp(self):
                    
        try:
            die_temp = self.sensor.readS16BE(ambient_reg) >> 2
        except:
            print("Error: unable to read die temperature")

        die_temp *= 0.03125        # Convert to celsius
        die_temp += 273.14         # Convert to kelvin
        return die_temp
    
    def read_obj_vol(self):
        try:
            obj_vol = self.sensor.readS16BE(object_vol_reg)
        except:
            print("Error: unable to read object voltage")

        obj_vol *= 156.25         # 156.25 nV per bit
        obj_vol /= 1000000000.0   # Convert nV to volts
        return obj_vol
    
    def get_temp(self):
        obj_vol = self.read_obj_vol()
        die_temp = self.read_die_temp()
        temp = self.calc_temp(die_temp, obj_vol)
        
        if temp < 0:
            raise Exception("Negative vemperature value - do not touch sensor")

        return temp

    def log_temp(self):
        temp = get_temp()
        data = {}
        data = {}
        data['temperature'] = []
        data['temperature'].append({
        'temperature': temp,
        'time':strftime("%a, %d %b %Y %H:%M", gmtime())
        })
        with open('data.txt', 'w') as outfile:
            json.dump(data, outfile)


if __name__ == "__main__":
    mytemp = Temp()
    mytemp.begin()
    temp = mytemp.get_temp()
    print(temp)
