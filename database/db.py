from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, select,insert,ForeignKey, func, DateTime

# create engine to connect to db
_engine = create_engine("mariadb+mariadbconnector://root@127.0.0.1:3306/greenhouse")
_meta = MetaData()

users = Table(
'users', _meta, 
Column('id', Integer, primary_key = True, nullable=False, autoincrement=True, unique=True), 
Column('username', String(45), nullable=False, unique=True), 
Column('password', String(128), nullable=False),
Column('role', String(64), nullable=False) 
)
greenhouse = Table(
    'greenhouse', _meta,
    Column('id', Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
)
greenhouseData = Table(
    'greenhouseData', _meta,
    Column('entry_id', Integer, primary_key=True, nullable=False, autoincrement=True, unique=True),
    Column('greenhouse_ID', Integer, ForeignKey("greenhouse.id"), nullable=False),
    Column('create_time', DateTime, server_default=func.now()),
    Column('light_level', String(10), nullable=False),
    Column('humidity', Integer, nullable=False),
    Column('temperature', Integer, nullable=False)
)
_meta.create_all(_engine)

def insertScheduledData(_greenhouse, _lightlevel, _humidity, _temperature):
    _stmt = insert(greenhouseData).values(greenhouse_ID = _greenhouse, light_level = _lightlevel, humidity = _humidity, temperature = _temperature)
    try:
        _conn = _engine.connect()
        _conn.execute(_stmt)
        _conn.commit()
        _conn.close()
    except:
        print('Something went wrong with inserting the scheduled data')

