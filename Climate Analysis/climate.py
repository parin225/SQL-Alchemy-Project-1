#import sqlalchemy
import sqlalchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#import Flask
from flask import Flask, jsonify

#import datetime
import datetime as dt

#database setup
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

#reflect an exisiting database into a new model
Base = automap_base()

#reflect the tables
Base.prepare(engine, reflect=True)

#save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#create session link from Python to database
session = Session(engine)

#create an app, passing __name__
app=Flask(__name__)

#create home page, listing all routes available
@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

#convert precipitation results into dictionary 
@app.route("/api/v1.0/precipitation")
def precipitation():
    #retrieve the last 12 months of precipitation data 
    twelve_months_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

    #retrieve only the date and precipitation vales
    query = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= twelve_months_ago).\
    order_by(Measurement.date).all()

    #create dictionary
    precipitation = dict(query) 
    
    return jsonify(precipitation)

#create a JSON list of stations from the dataset
@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Station.station).\
    group_by(Station.station).all()
    
    return jsonify(stations)

#create a JSON list of temperature observations for the previous year 
#from last data point set
@app.route("/api/v1.0/tobs")
def tobs():
    #retrieve the last 12 months of temperature observation data
    twelve_months_temp = dt.date(2017,8,23) - dt.timedelta(days=365)

    #retrieve temperature observation data\
    query = session.query(Measurement.date, Measurement.tobs).\
    filter (Measurement.date >= twelve_months_temp).\
    order_by(Measurement.date).all()

    return jsonify(query)

#create a JSON list of min., max. and avg. temp. for any dates >= start date
@app.route("/api/v1.0/<start>")
def start_date(start):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).all()
    
    return jsonify(results)

#create a JSON list of min., max. and avg. temp. for given start and end dates
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start,end):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True) 