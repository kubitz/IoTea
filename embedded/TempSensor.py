
import glob
import time
import paho.mqtt.client as mqtt

class DS18B20: 
    def __init__(self): 
        """ Initialises directory to folder containing file with result of sensor
            This path should not be changed for use with raspberry pi
        """
        self.base_dir = '/sys/bus/w1/devices/'
        self.device_folder = glob.glob(self.base_dir + '28*')[0]
        self.device_file = self.device_folder + '/w1_slave'

    def get_temp(self):
        """ Extracts temperature in degree Celsius from the  w1_slave file (located after "t=")
            Input: file directory (class attribute)
            Output: Temperature in degree Celsius
        """
        lines = self._get_temp_raw()

        while not self._is_successful_read(lines):
            time.sleep(0.2)
            lines = self._get_temp_raw()
        
        try: 
            temp_file_location = lines[1].find('t=')
        except: 
            print("ERROR: w1_slave file corrupted. No t= found.")
        
        if temp_file_location is not -1:
            temp_string = lines[1][temp_file_location+2:]
            temp = float(temp_string) / 1000.0
            return temp

    def _is_successful_read(self, lines): 
        """ Checks if the w1_slave file contains a successful temp read 
            Input: lines from ws1_slave file (list of strings)
            Output: 1 if successful read, 0 otherwise
        """
        if (lines[0].strip()[-3:]) != 'YES': 
            return 0
        return 1
    
    def _get_temp_raw(self):
        """ Extracts lines from w1_slave file that contains the OneWire result
            Input: file directory (class attribute)
            Output: list of string. Each string contains a line. 
        """
        try: 
            f = open(self.device_file, 'r')
            lines = f.readlines()
            f.close()
            return lines

        except: 
            print("ERROR: w1_slave file could not be opened (temp sensor)")


if __name__ == "__main__":
    #client = mqtt.Client()
    array = []
    time = []
    count = 0
    while True: 
        count += 1
        temp_sensor = DS18B20()
        array.append(temp_sensor.get_temp())
        time.append(count)
        print(array)
        print(time)
        time.sleep(3)
    #client.connect("test.mosquitto.org", port=1883)
    #client.publish("IC.embedded/IoTea/test", str(temp))
 
    

