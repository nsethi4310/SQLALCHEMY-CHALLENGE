import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""

    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitations<br/>"
        f"/api/v1.0/Stations<br/>"
        f"/api/v1.0/Temperature<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"

    )


@app.route("/api/v1.0/precipitations")
def prcp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #max_date=session.query(measurement.date).order_by(measurement.date.desc()).first()
    #year_ago= dt.date(2017,8,23)- dt.timedelta(days=365)
#session.query(measurement.date, measurement.prcp).filter(measurement.date >= year_ago).all()
# # Perform a query to retrieve the data and precipitation scores
    prcp_scores=session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >="2016-08-23").all()
    
    session.close()

    # Convert list of tuples into normal list
    all_scores = []
    for date, prcp in prcp_scores:
        prcp_dict = {}
        prcp_dict["Dates"]=date
        prcp_dict["prcp"]=prcp
        
        all_scores.append(prcp_dict)
        
    return jsonify(all_scores)


@app.route("/api/v1.0/Stations")
def Stat_details():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    station1 = session.query(Station.id, Station.name, Station.station, Station.longitude, Station.latitude, Station.elevation).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_station = []
    for id, name, station, lat, lng, elve in station1:
        station_dict = {}
        station_dict["ID"] = id
        station_dict['Station']=station
        station_dict["Name"] = name
        station_dict["latitude"] = lat
        station_dict["longitude"] = lng
        station_dict["elevation"] = elve

        all_station.append(station_dict)

    return jsonify(all_station)
@app.route("/api/v1.0/Temperature")
def temp():
#     # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query temp
    temp = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station=='USC00519281').filter(Measurement.date >= "2016-08-23").all()
    
    session.close()

    # Create a dictionary from the row data and append 
    all_temp = []
    for date, temps in temp:
        temp_dict = {}
        temp_dict["Date"] = date
        temp_dict['Tempartature']= temps
        
        all_temp.append(temp_dict)

    return jsonify(all_temp)
@app.route("/api/v1.0/<start>")
def st_date(start):
    session = Session(engine)
    results= session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    session.close()
    return jsonify(results)
@app.route("/api/v1.0/<start>/<end>")
def end_date(start,end):
    session = Session(engine)
    results= session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
    return jsonify(results)
if __name__ == '__main__':
    app.run(debug=True)
