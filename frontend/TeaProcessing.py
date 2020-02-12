import math

AVERAGE_TEACUP_CONSTANT = 13100
AVERAGE_ROOM_TEMP = 25

def predict_teacup_temp(current_temp, final_temp): 
    """ Predict the time in seconds left to reach the desired temperature
        Based on average time constant of a teacup, and 25°C room temp
        Input: current temperature , final desired temperature
        Output: predicted time in seconds until the teacup reaches the desired temperature
    """
    if (int(final_temp) < AVERAGE_ROOM_TEMP): 
        print("ERROR: final temperature cannot be under average room temp")
        return Exception


    time_left  = - (AVERAGE_TEACUP_CONSTANT/AVERAGE_ROOM_TEMP) * math.log((float(final_temp) - AVERAGE_ROOM_TEMP)/(float(current_temp) - AVERAGE_ROOM_TEMP))
    return time_left

def is_sensor_ready(list_of_temps): 
    """ Check if the sensor is ready to make a prediction
        The sensor is ready if it is compeletly heated up 
        and the temperature stopped increasing
        Input: matched list of temperatures ordered by time of recording
        Output: 1 if the sensor is ready, 0 otherwise
    """
    number_readings = len(list_of_temps)
    if (number_readings < 2):
        print("ERROR: at least two readings are needed to check if sensor is ready") 
        return Exception
    else: 
        last_two_reads = list_of_temps[-2:]

        if (last_two_reads[0] > last_two_reads[1]): 
            return 0
        else:
            return 1
    

if __name__ == "__main__":
    final_temp = input("Enter final temperature: ")
    current_temp = input("Enter Current temperature: ")
    print("Predicted time in seconds is: ", predict_teacup_temp(current_temp,final_temp))