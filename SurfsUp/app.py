#imports for operation of the app
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from datetime import datetime, timedelta 

from flask import Flask, jsonify

#Setting up engine for communication between python and sqlite
engine = create_engine("sqlite:///../Resources/hawaii.sqlite", echo=False)

# Reflects existing database into new model
Base = automap_base()

# Reflect tables
Base.prepare(autoload_with=engine)

#Sets classesn from database
Measurement = Base.classes.measurement
Station = Base.classes.station

#Establishes connection
app = Flask(__name__)

#Home Page
@app.route("/")
def home():
    return (
        f"Welcome to the Hawaii climate app!</br>"
        f"</br>"
        f"<p>Directions:</p></br>"
        f"Paste the desired string onto the end of your current URL for selected precipitation, weather station, and temperature data.</br>"
        f"</br>"
        f"/api/v1.0/precipitation</br>"
        f"/api/v1.0/stations</br>"
        f"/api/v1.0/tobs</br>"
        f"</br>"
        f"To query minimum, average, and maximum values, add the start date in form XXXX-XX-XX to the below URL and append it to the end of your current URL. If you would like to specify and end date, add an end date to the end in the form /XXXX-XX-XX .</br>"
        f"</br>"
        f"/api/v1.0/"
    )
#Queries precipitation data
@app.route("/api/v1.0/precipitation")
def precip():
    session = Session(engine)
    
    year_precipitation = session.query(Measurement.date, Measurement.prcp)\
        .filter(Measurement.date >= datetime.strptime(session.query(func.max(Measurement.date))\
        .scalar(), '%Y-%m-%d').date() - dt.timedelta(days=365))\
        .order_by(Measurement.date.asc()).all()

    
    session.close()
    
    precip = dict((i, j) for i, j in year_precipitation)

    #Note here that converting tuple to dictionary as per instructions cuts off all but the last 
    #value in each date. To retain all values, pass the tuple created as "year_precipitation" directly
    #to the return by changing below line to data_plot = list(np.ravel(year_precipitation))
    data_plot = list(np.ravel(precip))

    return jsonify(data_plot)

#Queries stations data
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    most_active_stations = sorted(session.query(Measurement.station, func.count(Measurement.station)).\
                         group_by(Measurement.station).all(), key = lambda x: x[1], reverse=True)
    
    session.close()

    station_plot = list(np.ravel(most_active_stations))

    return jsonify(station_plot)

#Queries temperature data
@app.route("/api/v1.0/tobs")
def temps():
    session = Session(engine)

    most_active_station_id = sorted(session.query(Measurement.station, func.count(Measurement.station)).\
                         group_by(Measurement.station).all(), key = lambda x: x[1], reverse=True)[0][0]
    
    year_temperature = session.query(Measurement.date, Measurement.tobs)\
        .filter(Measurement.date >= datetime.strptime(session.query(func.max(Measurement.date))\
        .scalar(), '%Y-%m-%d').date() - dt.timedelta(days=365))\
        .filter(Measurement.station == most_active_station_id).all()
    
    session.close()

    temp_plot = list(np.ravel(year_temperature))
    
    return jsonify(temp_plot)

#Queries by a start date until the end of the data
@app.route("/api/v1.0/<start>")
def query_from_start(start):
    session = Session(engine)
    
    statistics_start = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
           .filter(Measurement.date >= start ).all()
    #As per instructions, method returns a list. For a dictionary representation, substitute below code:
    #output = { "min_temp" : statistics_start[0][0], "avg_temp" : round(statistics_start[0][1], 1), "max_temp" : statistics_start[0][2]}
    output = (statistics_start[0][0], round(statistics_start[0][1], 1), statistics_start[0][2])

    session.close()

    return jsonify(output)

#Queries by a start and end date
@app.route("/api/v1.0/<start>/<end>")
def query_start_to_end(start, end):
    session = Session(engine)

    statistics_start_end = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
            .filter(Measurement.date >= start)\
            .filter(Measurement.date <= end).all()
    #As per instructions, method returns a list. For a dictionary representation, substitute below code:
    #output = { "min_temp" : statistics_start_end[0][0], "avg_temp" : round(statistics_start_end[0][1], 1), "max_temp" : statistics_start_end[0][2]}
    output = (statistics_start_end[0][0], round(statistics_start_end[0][1], 1), statistics_start_end[0][2])

    
    session.close()

    return jsonify(output)

#Enables us to run only as script
if __name__ == "__main__":
    app.run(debug=True)
