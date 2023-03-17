from flask import Flask
from fhict_cb_01.CustomPymata4 import CustomPymata4
from apscheduler.schedulers.background import BackgroundScheduler
import requests

app = Flask(__name__)

#region global variables
board = CustomPymata4(com_port = "COM5")
ldrvalue = 0
humidity = 0
temperature = 0
LDRPIN = 2
DHTPIN  = 12
#endregion


#region air
def Measure(data):
    global humidity, temperature
    # [report_type, pin, dht_type, error_value, humidity, temperature, timestamp]
    if (data[3] == 0):
        humidity = data[4]
        temperature = data[5]
        
def air():
    global board
    board.displayOff()
    board.set_pin_mode_dht(DHTPIN, sensor_type=11, differential=.05, callback=Measure)
#endregion
#region LDR
def LDRChanged(data):
    global ldrvalue
    ldrvalue = data[2]

def ldr():
    board.set_pin_mode_analog_input(LDRPIN, callback = LDRChanged, differential = 10)
#endregion


ldr()
air()


def scheduledDataEntry():
    PostData = {'Greenhouse_number': 1 , 'Sensor_ID': 487498, 'light_level': ldrvalue, 'humidity': humidity,'temperature': temperature}
    response = requests.post('http://127.0.0.1:5000/data/entry', json=PostData)
    print(response.status_code)
sched = BackgroundScheduler()
sched.add_job(scheduledDataEntry, 'interval', seconds =10) #will do the scheduledDataEntry work for every 30 seconds

sched.start()