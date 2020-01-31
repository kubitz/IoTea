import Adafruit_GPIO.I2C as I2C
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
        self.sensor = I2C.get_i2c_device(pin_address)

    def begin(self):
        self.sensor.write16(config_reg, config_val)

    def calc_temp(self, TDie, Vobj):      
        Tdie_ref = Tdie - TREF
        S = 1.0 + A1*Tdie_ref + _A2*math.pow(Tdie_ref, 2.0)
        S *= S0
        S /= 10000000.0
        S /= 10000000.0
        Vos = B0 + B1*Tdie_ref + B2*math.pow(Tdie_ref, 2.0)
        fVobj = (Vobj - Vos) + C2*math.pow((Vobj - Vos), 2.0)
        Tobj = math.sqrt(math.sqrt(math.pow(Tdie, 4.0) + (fVobj/S)))
        return Tobj - 273.15

    def read_die_temp(self):
        die_temp = self.sensor.readS16BE(ambient_reg) >> 2
        die_temp *= 0.03125        # Convert to celsius
        die_temp += 273.14         # Convert to kelvin
        return die_temp
    
    def read_obj_vol(self):
        obj_vol = self.sensor.readS16BE(object_vol_reg)
        obj_vol *= 156.25         # 156.25 nV per bit
        obj_vol /= 1000000000.0   # Convert nV to volts
    
    def get_temp(self):
        obj_vol = self.read_obj_vol()
        die_temp = self.read_die_temp()
        temp = self.calc_temp(die_temp, obj_vol)
        return temp

       
mytemp = Temp()
mytemp.begin()
mytemp.get_temp()
print(temp)
