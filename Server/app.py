from flask import Flask, render_template, request
from database import db
import json
import requests



#region global variables
app = Flask(__name__)
#endregion

@app.route("/data")
def datapage():
    amount = request.args.get('amount', default=10, type=int)
    greenhouse = request.args.get('greenhouse', default=1, type=int)
    return db.getLatestData(greenhouse, amount)
@app.route("/data/greenhouses")
def dataGreenhouses():
    return db.getGreenhouses()
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
@app.route("/data/entry" , methods = ['POST'])
def receive_data():
    data = request.get_json()
    print(data)
    Greenhouse_number = data['Greenhouse_number']
    Sensor_ID = data['Sensor_ID']
    light_level = data['light_level']
    humidity = data['humidity']
    temperature = data['temperature']

    try:
        db.insertScheduledData(Greenhouse_number, Sensor_ID,light_level,humidity,temperature)
        return "Data has been entered"
    except:
        print('something went wrong with inserting the data')


@app.route("/greenhouse/")
def page():
    greenhouse = request.args.get('greenhouse')
    responseData = requests.get("http://127.0.0.1:5000/data?greenhouse=" + greenhouse + "&amount=10")
    data = json.loads(responseData.text)
    responseAverages = requests.get("http://127.0.0.1:5000/data/averages?greenhouse=" + greenhouse)
    dataAverage = json.loads(responseAverages.text)
    responseLowest = requests.get("http://127.0.0.1:5000/data/minimum?greenhouse=" + greenhouse)
    dataLowest = json.loads(responseLowest.text)
    responseHighest = requests.get("http://127.0.0.1:5000/data/highest?greenhouse=" + greenhouse)
    dataHighest = json.loads(responseHighest.text)
    return render_template('data.html', readingsfromdatabase=data, AverageData=dataAverage, LowestData=dataLowest, HighestData=dataHighest)

@app.route("/dev")
def dev():
    return render_template('base.html')