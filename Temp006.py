import Adafruit_GPIO.I2C as I2C

    
pin_address = 0x40  #adress location for RPi I2C
config_reg = 0x02    #register address for configuration data
object_vol = 0x0
 
config_val = 0x79  #Device in active mode, output low (I think), 16 samples


class Temp():

 
    def __init__(self):
        self.temperature = 0
        self.time = 0
        self.sensor = I2C.get_i2c_device(pin_address)

    def begin(self):
        self.sensor.write16(config_reg, config_val)
    
    def get_temp(self):
        ambient = self.sensor.readS16BE(object_vol)
        print(ambient)


mytemp = Temp()
mytemp.begin()
mytemp.get_temp()



