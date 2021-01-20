from flask import Flask, jsonify
import numpy as np
import pandas as pd
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

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
Stations = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

last_twelve_months = '2016-08-23'

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"

    )


@app.route("/api/v1.0/precipitation")    
def precipitation():
    last_yr = dt.date(2017,8,23) - dt.timedelta(days = 365)
    last_day = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > last_yr).order_by(Measurement.date).all()

#Convert the query results to a Dictionary using date as the key and prcp as the value.
#Return the JSON representation of your dictionary.
    precipitation_data = []
    for i in precipitation:
        data = {}
        data['date'] = precipitation[0]
        data['prcp'] = precipitation[1]
        precipitation_data.append(data)
    return jsonify(precipitation_data)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Return a JSON list of stations from the dataset.
    station_results = session.query(Stations.station).all()
    # station_all = list(np.ravel(station_results))
    session.close()
    return jsonify(station_results)

        

@app.route("/api/v1.0/tobs")
def tobs():
     # Create our session (link) from Python to the DB
    session = Session(engine)

    # Return a JSON list of Temperature Observations (tobs) for the previous year
    all_tobs = session.query(Measurement.date, Measurement.station, Measurement.tobs).filter(Measurement.date >= last_twelve_months).all()
    session.close()
    return jsonify(all_tobs)

@app.route("/api/v1.0/start")
def startDateOnly(date):

# Create our session (link) from Python to the DB
    session = Session(engine)

    # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    # When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    day_temp_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= date).all()
    session.close()
    return jsonify(day_temp_results)

@app.route("/api/v1.0/start/end")
def startDateEndDate(start,end):

    # Create our session (link) from Python to the DB
    session = Session(engine)
    #  Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    #  When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
    multi_day_temp_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
    return jsonify(multi_day_temp_results)

if __name__ == '__main__':
    app.run(debug=True)
