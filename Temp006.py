import Adafruit_GPIO.I2C as I2C
class Temp():
    
    pin_address = 0x40  #adress location for RPi I2C
    config_reg = 0x02    #register address for configuration data
    object_vol = 0x0

    #Device in active mode, output low (I think), 16 samples
    config_val = 0x79

    def __init__(self):
        self.temperature
        self.time
        self.sensor = I2C.get_i2c_device(pin_address, **kwargs)

    def begin(self):
        self.sensor.write16(config_reg, config_val)
    
    def get_temp(self):
        ambient = self.sensor.readS16BE(object_vol)



