import time
import random

# temp things for testing

def is_talking():
    time.sleep(1)
    if random.randint(1,12) == 4:
        print("True")
        return True
    else:
        return False

def get_convo():
    print "Begin Analysis"
    time.sleep(10)
    print "End Analysis"

    i = random.randint(40, 60)

    if i > 50:
        return "good"
    else:
        return "bad"

def get_time():
    temp = int(round(time.time() * 1000))
    return temp

oldTime = 0
def get_flag(interval):
    global oldTime
    newTime = get_time()
    if newTime - oldTime > interval:
        oldTime = newTime
        return True
    else:
        return False


def get_temp():
   return random.randint(40, 60)


def main():
    status = "good"
    while True:
        print("Main Loop")
        if is_talking() == True:
            status = get_convo()
        if get_flag(5000) == True:
            temp = get_temp()
            print("Status " + status + " temperature =" + str(temp))


main()




