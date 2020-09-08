import numpy as np
import webbrowser

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify




################################-----------------################################################
################################ USER ENTERED START DATE#########################################

# Prompt User to select START DATE. We will also put in place functions to ensure valid responses
print("So you're going to Hawaii, huh? Let's see what the weather looks like!")
def get_start_date(prompt):
    while True:
        try:
            start_day1 = int(input("Put in the start day of your holiday (DD): "))
        except ValueError:
            print("Sorry, please enter a valid number")
            continue

    #continue to prompt the user to pick a valid date and not leave blank
        if start_day1<1 or start_day1>31:
            print("Sorry, please provide a valid date as a 2 digit value (DD)")
            continue
        else:
    #Date range is in the appropriate range(1-31)
            break
    return start_day1

start_day1 = get_start_date("Put in the starting day of your holiday (DD): ")
start_day=str(format(start_day1, '02d'))



def get_start_month(prompt):
    while True:
        try:
            start_month1 = int(input("Put in the starting month number of your holiday (MM): "))
        except ValueError:
            print("Sorry, please enter a valid number")
            continue

    #continue to prompt the user to pick a valid date and not leave blank
        if start_month1<1 or start_month1>12:
            print("Sorry, please provide a valid month number")
            continue    
        else:
    #Date range is in the appropriate range(1-31)
            break
    return start_month1

start_month1= get_start_month("Put in the starting month of your holiday (MM): ")
start_month=str(format(start_month1, '02d'))

#Determine start year of holiday
if (start_day1 < 23 and start_month1 < 8):
    start_year="2017"
else:
    start_year="2016"

#Final Start date for reference wth our database
start_date= start_year+"-"+start_month+"-"+start_day

#START date for reference in our database
print(f"Your holiday start date is {start_date}")

################################-----------------------###########################################
################################ USER ENTERED END DATE ###########################################

def get_end_date(prompt):
    while True:
        try:
            end_day1 = int(input("Put in the end date of your holiday (DD), or leave blank and hit ENTER: ") or "23")
        except ValueError:
            print("Sorry, please enter a valid number")
            continue

    #continue to prompt the user to pick a valid date and not leave blank
        if end_day1<1 or end_day1>31:
            print("Sorry, please provide a valid date")
            continue  
        else:
    #Date range is in the appropriate range(1-31)
            break
    return end_day1

end_day1 = get_end_date("Put in the final day of your holiday (DD), or leave blank and hit ENTER: ")
end_day=str(format(end_day1, '02d'))


def get_end_month(prompt):
    while True:
        try:
            end_month1 = int(input("Put in the number of your last month of holidays (MM), or leave blank and hit ENTER ") or "08")
        except ValueError:
            print("Sorry, please enter a valid number")
            continue

    #continue to prompt the user to pick a valid date and not leave blank
        if end_month1<1 or end_month1>12:
            print("Sorry, please provide a valid month number")
            continue        
        else:
    #Date range is in the appropriate range(1-31)
            break
    return end_month1

end_month1= get_end_month("Put in the final month of your holiday (MM), or leave blank and hit ENTER: ")
end_month=str(format(start_month1, '02d'))

#Determine end year of holiday
end_year="2017"

end_date= end_year+"-"+end_month+"-"+end_day


#END date for reference in our database
print(f"Your holiday end date is {end_date}")


#Determine the route for start and end dates, based on user input above
api_route= start_date+"/"+end_date


#Show a message in command console, and then open home page with routes
print("Please go to you browser to see information about the weather during your stay")
webbrowser.open("http://127.0.0.1:5000/")


#end_date= input("Put in the end of your holiday, or leave blank: YYYY-MM-DD ")











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
clima_app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@clima_app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<{start_date}><br/>"
        f"/api/v1.0/<{api_route}><br/>"
    )

@clima_app.route("/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Daily rainfall over last 12 months"""
    # Query all rainfall data from database, and then give average rainfall across Hawaii
    results = session.query(Measurement.date, func.avg(Measurement.prcp)).\
    filter(Measurement.date >= '2016-08-23').\
    filter(Measurement.date <= '2017-08-23').\
    group_by(Measurement.date).\
    order_by(Measurement.date).all()

    session.close()

    # Create a dictionary for precipitation data
    all_rainfall = []
    for date, prcp in results:
       rainfall_dict = {}
       rainfall_dict["date"] = date
       rainfall_dict["rainfall"] = prcp
       all_rainfall.append(rainfall_dict)

    return jsonify(all_rainfall)


@clima_app.route("/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Daily rainfall over last 12 months"""
    # Query all stations and return their names
    station_names = session.query(Station.name).\
    order_by(Station.name).all()

    session.close()

    # Convert list of tuples into normal list
    station_list = list(np.ravel(station_names))

    return jsonify(station_list)

@clima_app.route("/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)


    """tobs observations count"""
    # Query merging station names with measurement data, returning station id of station with most observations, and returning as a string
    station_data1=session.query(Station.station).\
    filter(Measurement.station == Station.station).\
    group_by(Station.station).\
    order_by(func.count(Measurement.tobs).desc()).first()
    
    filter_set=list(station_data1)
    #tuples_filtered = [tup for tup in tuples if tup[0] in filter_set]
    #tuples_filtered
    max_station=str(filter_set[0])
    max_station
    type(max_station)


    """tobs observations"""
    # Query merging station names with measurement data, returning observations for most active staion
    station_data2=session.query(Measurement.station, Measurement.date, Measurement.tobs, Station.name).\
    filter(Measurement.station == Station.station).\
    filter(Measurement.station == max_station).\
    filter(Measurement.date >= '2016-08-23').\
    filter(Measurement.date <= '2017-08-23').\
    order_by(Measurement.date.desc()).all()

    session.close()

    # Convert list of tuples into normal list
    tobs_list = list(np.ravel(station_data2))

  
    return jsonify(tobs_list)


@clima_app.route(f"/{start_date}")
def start():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Temperature over last months"""
    # Query all data
    results = session.query(func.avg(Measurement.tobs), func.min(Measurement.tobs),func.max(Measurement.tobs)).\
    filter(Measurement.date >= start_date).\
    filter(Measurement.date <= "2017-08-23").all()
    #group_by(Measurement.date).\
    #order_by(Measurement.date).all()

    session.close()

    # Create a dictionary for precipitation data
    all_temps = []
    for avg_temp, min_temp, max_temp in results:
       temp_dict = {}
       temp_dict["avg_temp"] = avg_temp
       temp_dict["min_temp"] = min_temp
       temp_dict["max_temp"] = max_temp

       all_temps.append(temp_dict)

    return jsonify(all_temps)


@clima_app.route(f"/{api_route}")
def start_end():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Temperature over last months"""
    # Query all data
    results = session.query(func.avg(Measurement.tobs), func.min(Measurement.tobs),func.max(Measurement.tobs)).\
    filter(Measurement.date >= start_date).\
    filter(Measurement.date <= end_date).all()
    #group_by(Measurement.date).\
    #order_by(Measurement.date).all()

    session.close()

    # Create a dictionary for precipitation data
    all_temps = []
    for avg_temp, min_temp, max_temp in results:
       temp_dict = {}
       temp_dict["avg_temp"] = avg_temp
       temp_dict["min_temp"] = min_temp
       temp_dict["max_temp"] = max_temp

       all_temps.append(temp_dict)

    return jsonify(all_temps)

if __name__ == '__main__':
   clima_app.run(debug=False)
