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

def scheduledDataEntry():
    db.insertScheduledData(1,ldrvalue,humidity,temperature)

sched = BackgroundScheduler()
sched.add_job(scheduledDataEntry, 'interval', seconds =30) #will do the scheduledDataEntry work for every 30 seconds

sched.start()

@app.route("/data")
def datapage():
    amount = request.args.get('amount', default=10, type=int)
    greenhouse = request.args.get('greenhouse', default=1, type=int)
    return db.getLatestData(greenhouse, amount)
@app.route("/data/averages")
def dataAveragespage():
    greenhouse = request.args.get('greenhouse', default=1, type=int)
    return db.getAverageData(greenhouse)
@app.route("/data/minimum")
def dataLowestpage():
    greenhouse = request.args.get('greenhouse', default=1, type=int)
    return db.getLowestData(greenhouse)
@app.route("/data/highest")
def dataHighestpage():
    greenhouse = request.args.get('greenhouse', default=1, type=int)
    return db.getHighestData(greenhouse)

@app.route("/")
def page():
    responseData = requests.get("http://127.0.0.1:5000/data?greenhouse=1&amount=10")
    data = json.loads(responseData.text)
    responseAverages = requests.get("http://127.0.0.1:5000/data/averages?greenhouse=1")
    dataAverage = json.loads(responseAverages.text)
    responseLowest = requests.get("http://127.0.0.1:5000/data/minimum?greenhouse=1")
    dataLowest = json.loads(responseLowest.text)
    responseHighest = requests.get("http://127.0.0.1:5000/data/highest?greenhouse=1")
    dataHighest = json.loads(responseHighest.text)
    return render_template('data.html', readingsfromdatabase=data, AverageData=dataAverage, LowestData=dataLowest, HighestData=dataHighest)