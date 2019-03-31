# Dependencies 
# FLASK app for generating Weather data to JSON-ified API
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


# Create an engine to a SQLite database file 
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to each tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Setup Flask app
app = Flask(__name__)

# Query for the dates and precipitation values 
# Convert the query results to a Dictionary using date as the key and tobs as the value.
# Return the json representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Retrieve a list of date and precipitation from last year 
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').order_by(Measurement.date)
    
    # Create a dictionary from the row data and append to a list
    precipitation_values = []
    for p in results:
        prcp_dict = {}
        prcp_dict["date"] = p.date
        prcp_dict["prcp"] = p.prcp
        precipitation_values.append(prcp_dict)

    return jsonify(precipitation_values)


# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    # Retrieve a list of station names and query all stations
    stations = session.query(Station.name).all()

    # Convert list of tuples into normal list
    station_names = list(np.ravel(stations))

    return jsonify(station_names)

# Return a json list of Tobs for the previous year
@app.route("/api/v1.0/tobs")
def tobs():
    # Retrieve a list of Tobs and query all tobs values
    results = session.query(Measurement.tobs).all()

    # Convert list of tuples into normal list
    tobs_value = list(np.ravel(results))

    return jsonify(tobs_value)

# Return a JSON list of the minimum temperature, the average temperature, and the max temperature.
# With a given start or start-end range
@app.route("/api/v1.0/<start>")
def temperatures_start(start):
    
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).all()
    
    # Convert list of tuples into normal list
    temp_start = list(np.ravel(results))

    return jsonify(temp_start)
.
@app.route("/api/v1.0/<start>/<end>")
def temperatures_end(start, end):
   
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                filter(Measurement.date <= end).all()
    
    # Convert list of tuples into normal list
    temperatures_end = list(np.ravel(results))

    return jsonify(temperatures_end)


if __name__ == "__main__":
    app.run(debug=True)

