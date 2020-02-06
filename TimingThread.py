import threading
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
        print "good"
    else:
        print "bad"
    threading.Timer(1, get_convo).start()

def get_temp():
   print random.randint(40, 60)
   threading.Timer(1, get_temp).start()


get_temp()
get_convo()