from flask import Flask, render_template, request
from fhict_cb_01.CustomPymata4 import CustomPymata4
from random import randint
from datetime import datetime
from database import db
import json
import requests
from apscheduler.schedulers.background import BackgroundScheduler


#region global variables
app = Flask(__name__)
app.debug = True
board = CustomPymata4(com_port = "COM3")
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
LatestReadings = []

def scheduledDataEntry():
    db.insertScheduledData(1,ldrvalue,humidity,temperature)

sched = BackgroundScheduler()
sched.add_job(scheduledDataEntry, 'interval', seconds =30) #will do the scheduledDataEntry work for every 30 seconds

sched.start()

def get_data():
    date = datetime.now()
    now = date.strftime("%d/%m/%Y, %H:%M:%S")
    ldrlevel = ldrvalue
    lightandtime = str(ldrlevel) + ' W/M2 ' + now
    LatestReadings.append(lightandtime)
    if len(LatestReadings) > 25:
        LatestReadings.pop(0)
    return LatestReadings#, now

@app.route("/data")
def datapage():
    amount = request.args.get('amount', default=10, type=int)
    greenhouse = request.args.get('greenhouse', default=1, type=int)
    return db.getLatestData(greenhouse, amount)
    # return render_template('index.html', lightlevelandtime=Readings, ldr=ldrlevel, humidity=humidity, temperature=temperature )

@app.route("/")
def page():
    response = requests.get("http://127.0.0.1:5000/data?greenhouse=1&amount=10")
    data = json.loads(response.text)
    return render_template('data.html', readingsfromdatabase=data)