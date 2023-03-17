from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, select,insert,ForeignKey, func, DateTime
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
import json

# create engine to connect to db
_engine = create_engine("mariadb+mariadbconnector://root@127.0.0.1:3306/greenhouse")
Session = sessionmaker(bind=_engine)
if not database_exists(_engine.url):
    create_database(_engine.url)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(45), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    role = Column(String(64), nullable=False)
    
class Greenhouse(Base):
    __tablename__ = 'greenhouses'
    
    id = Column(Integer, primary_key=True, autoincrement=True)

class GreenhouseData(Base):
    __tablename__ = 'greenhouse_data'
    
    entry_id = Column(Integer, primary_key=True, autoincrement=True)
    greenhouse_id = Column(Integer, ForeignKey('greenhouses.id'), nullable=False)
    sensor_id = Column(Integer, nullable=False)
    create_time = Column(DateTime, server_default=func.now(), nullable=False)
    light_level = Column(Integer, nullable=False)
    humidity = Column(Integer, nullable=False)
    temperature = Column(Integer, nullable=False)
    
    greenhouse = relationship("Greenhouse", backref="data")
Base.metadata.create_all(_engine)

def insertScheduledData(_greenhouse, _sensor_id, _lightlevel, _humidity, _temperature):
    session = Session()
    Sensor_data = GreenhouseData(greenhouse_id = _greenhouse, sensor_id= _sensor_id ,light_level=_lightlevel, humidity=_humidity, temperature=_temperature)
    session.add(Sensor_data)
    session.commit()
    session.close()

def getLatestData(_id, _amount):
    session = Session()
    queryData = session.query(GreenhouseData).where(GreenhouseData.greenhouse_id == _id).order_by(GreenhouseData.create_time.desc()).limit(_amount).all()
    results = []   
    for record in queryData:
        results.append({
            'Greenhouse_number': record.greenhouse_id,
            'Sensor_ID': record.sensor_id,
            'time': record.create_time.strftime('%d-%m-%y %H:%M:%S'),
            'light_level': record.light_level,
            'humidity': record.humidity,
            'temperature': record.temperature
        })
    jsonified_results = json.dumps({'results': results})
    session.close()
    return jsonified_results

def getAverageData(_id):
    session = Session()
    queryData = session.query(
        func.avg(GreenhouseData.light_level),
        func.avg(GreenhouseData.humidity),
        func.avg(GreenhouseData.temperature)
        ).filter(
            GreenhouseData.greenhouse_id == _id
        ).one()
    session.close()  
    results = []
    results.append({
        'average_light_Level': str(queryData[0]),
        'average_humidity': str(queryData[1]),
        'average_temperature': str(queryData[2]),
    })
    jsonified_results = json.dumps({'results': results})
    return jsonified_results

def getLowestData(_id):
    session = Session()
    queryData = session.query(
        func.min(GreenhouseData.light_level),
        func.min(GreenhouseData.humidity),
        func.min(GreenhouseData.temperature)
        ).filter(
            GreenhouseData.greenhouse_id == _id
        ).one()
    session.close()  
    results = []
    results.append({
        'lowest_light_Level': str(queryData[0]),
        'lowest_humidity': str(queryData[1]),
        'lowest_temperature': str(queryData[2]),
    })
    jsonified_results = json.dumps({'results': results})
    return jsonified_results

def getHighestData(_id):
    session = Session()
    queryData = session.query(
        func.max(GreenhouseData.light_level),
        func.max(GreenhouseData.humidity),
        func.max(GreenhouseData.temperature)
        ).filter(
            GreenhouseData.greenhouse_id == _id
        ).one()
    session.close()  
    results = []
    results.append({
        'highest_light_Level': str(queryData[0]),
        'highest_humidity': str(queryData[1]),
        'highest_temperature': str(queryData[2]),
    })
    jsonified_results = json.dumps({'results': results})
    return jsonified_results