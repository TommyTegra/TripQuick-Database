from flask import Flask, render_template, json, redirect, request, jsonify
from flask_mysqldb import MySQL
import sys
import os

    # Note: Various parts of this file contains citations for certain parts of code.
    #   Citations are found typically right above the code of interest.
    #   Citations for starter code:
    #   Date: 11/09/2023
    #   Based on: [redacted] Flask guide, Layout/Template with the exception of functions and queries. Specific details below.
    #   Source URL: [redacted]
    #   Source URL: [redacted] 

app = Flask(__name__)

# app.config['MYSQL_HOST'] = [redacted]
# app.config['MYSQL_USER'] = [redacted]
# app.config['MYSQL_PASSWORD'] = [redacted]
# app.config['MYSQL_DB'] = [redacted]
# app.config['MYSQL_CURSORCLASS'] = "DictCursor"


mysql = MySQL(app)

# These functions are original designs to solve a problem with HTML and forms handlingreserved characters
def reserved(data):
    """
    replaces hmtl reserved characters with html entity names
    """
    for item_num, item in enumerate(data):
        for key in item.keys():
            if type(item[key]) is str:
                data[item_num][key] = item[key].replace("&", "&amp;")
                data[item_num][key] = item[key].replace('"', "&quot;")
                data[item_num][key] = item[key].replace("'", "&#8217;")  # &#8217 looks like an apostrophe &apos, but a real one messed with the code too much.
                data[item_num][key] = item[key].replace("<", "&lt;")
                data[item_num][key] = item[key].replace(">", "&gt;")
    return data



# Routes
@app.route('/')
def root():
    return render_template("index.j2")


# Traveler Entity 
    # Citation for the following POST/GET methods:
    # Date: 11/16/2023
    # Based on: [redacted]
    # Source URL: [redacted]
    # With the exception of query code and specifics such as variable names, etc. 
@app.route('/travelers', methods=["POST", "GET"])
def travelers():
    if request.method == "POST":
        # Insert
        if request.form.get("AddTraveler"):
            name = request.form["name"]
            email = request.form["email"]
            phone = request.form["phone"]

            query = "INSERT INTO Travelers (name, email, phone) VALUES (%s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (name, email, phone))
            mysql.connection.commit()

            return redirect("/travelers")
        
        # Update
        if request.form.get("UpdateTraveler"):
            name = request.form["name"]
            email = request.form["email"]
            phone = request.form["phone"]
            travelerID = request.form["travelerID"]

            query = "UPDATE Travelers SET name = %s, email = %s, phone = %s WHERE travelerID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (name, email, phone, travelerID))
            mysql.connection.commit()

            return redirect("/travelers")
        
        # Delete
        if request.form.get("DeleteTraveler"):
            travelerID = request.form["travelerID"]

            query = "DELETE FROM Travelers WHERE travelerID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (travelerID,))
            mysql.connection.commit()

            return redirect("/travelers")

    # Read
    if request.method == "GET":
        # Get all travelers
        query = "SELECT travelerID AS 'Traveler ID', name AS 'Name', email AS 'Email address', phone as 'Phone number' FROM Travelers"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = reserved(cur.fetchall())

    return render_template("travelers.j2", data=data)


# Itineraries Entity
    # Citation for the following POST/GET methods:
    # Date: 11/30/2023
    # Based on: [redacted] 
    # Source URL: [redacted] 
    # With the exception of query code, tuple manipulation, and specifics such as variable names, etc. 
@app.route('/itineraries', methods=["POST", "GET"])
def itineraries():
    if request.method == "POST":
        # Insert
        if request.form.get("InsertItinerary"):
            departureFlightID = request.form["departureFlightID"]
            returnFlightID = request.form["returnFlightID"]
            stayID = request.form["stayID"]
            home = request.form["home"]
            destination = request.form["destination"]
            assocTraveler = request.form["assocTraveler"]

            values = {
                "departureFlightID":    departureFlightID,
                "returnFlightID":       returnFlightID,
                "stayID":               stayID,
                "home":                 home,
                "destination":          destination,
                }
            
            # creates tuple of the values that exist; python retains order from dictionary
            values_tuple  = tuple([variable for variable in values.values() if variable])

            # creates a string for the query that only includes keys that aren't Null 
            query = "INSERT INTO Itineraries (departureFlightID, returnFlightID, stayID, home, destination) VALUES (" + ", ".join("%s" if values[key] else "NULL" for key in values.keys()) + ")"
            
            cur = mysql.connection.cursor()
            cur.execute(query, values_tuple)

            planID = cur.lastrowid

            query1 = """
            INSERT INTO Travelers_Itineraries (travelerID, planID)
            VALUES (%s, %s)
            """

            cur.execute(query1, (assocTraveler, planID))

            mysql.connection.commit()

            return redirect("/itineraries")
        
        # Update
        if request.form.get("UpdateItinerary"):
            departureFlightID = request.form["departureFlightID"]
            returnFlightID = request.form["returnFlightID"]
            stayID = request.form["stayID"]
            home = request.form["home"]
            destination = request.form["destination"]
            planID = request.form["planID"]

            values = {
                "departureFlightID":    departureFlightID,
                "returnFlightID":       returnFlightID,
                "stayID":               stayID,
                "home":                 home,
                "destination":          destination,
                }
            
            # creates tuple of the values that exist; python retains order from dictionary
            values_tuple  = tuple([variable for variable in values.values() if variable])

            # creates a string for the query that either uses passed value in tuple if value exists or hardcodes NULL otherwise
            sub_query = ""
            for num, key in enumerate(values.keys()):
                if num:
                    if values[key]:
                        sub_query += ", " + key + " = %s"
                    else:
                        sub_query += ", " + key + " = NULL"
                else:
                    if values[key]:
                        sub_query += key + " = %s"
                    else:
                        sub_query += key + " = NULL"

            query = "UPDATE Itineraries SET " + sub_query + " WHERE planID = %s"

            cur = mysql.connection.cursor()
            cur.execute(query, values_tuple + (planID,))
            mysql.connection.commit()

            return redirect("/itineraries")
        
        # Delete
        if request.form.get("DeleteItinerary"):
            planID = request.form["planID"]

            query = "DELETE FROM Itineraries WHERE planID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (planID,))
            mysql.connection.commit()

            return redirect("/itineraries")

    # Read
    if request.method == "GET":
        # Get all itineraries
        query = """
        SELECT
            Itineraries.planID AS 'Itinerary ID', 
            COALESCE(CONCAT(DepartureFlights.departing, ' to ', DepartureFlights.destination), 'None') AS 'Departure Ticket', 
            COALESCE(CONCAT(ReturnFlights.departing, ' to ', ReturnFlights.destination), 'None') AS 'Return Ticket', 
            COALESCE(Accommodations.propertyName, Accommodations.propertyAddress, 'None') AS 'Accommodation',
            Itineraries.home AS 'Home', 
            Itineraries.destination AS 'Destination' 
        FROM Itineraries
        LEFT JOIN Flights AS DepartureFlights ON DepartureFlights.flightID = Itineraries.departureFlightID 
        LEFT JOIN Flights AS ReturnFlights ON ReturnFlights.flightID = Itineraries.returnFlightID 
        LEFT JOIN Accommodations ON Accommodations.stayID = Itineraries.stayID
        """

        cur = mysql.connection.cursor()
        cur.execute(query)
        data = reserved(cur.fetchall())

        # Get dropdown for Flights
        query1 = """
        SELECT 
            flightID,
            CONCAT(departing, ' to ', destination) AS "Flights"
        FROM Flights
        """
        cur = mysql.connection.cursor()
        cur.execute(query1)
        flightData = reserved(cur.fetchall())

        # Get dropdown for Accommodations
        query2 = """
        SELECT
            stayID,
            CASE
                WHEN Accommodations.propertyName IS NULL THEN Accommodations.propertyAddress
                ELSE Accommodations.propertyName
            END AS 'Accommodations'
        FROM Accommodations
        """
        cur = mysql.connection.cursor()
        cur.execute(query2)
        stayData = cur.fetchall()

        # Get dropdown for Travelers
        query3 = "SELECT travelerID, name FROM Travelers"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        travelerData = reserved(cur.fetchall())

    return render_template("itineraries.j2", data=data, flightData=flightData, stayData=stayData, travelerData=travelerData)


# Flights Entity
    # Citation for the following POST/GET methods:
    # Date: 12/9/2023
    # Based on: [redacted]
    # Source URL: [redacted] 
    # With the exception of query code and specifics such as variable names, etc. 
@app.route('/flights', methods=["POST", "GET"])
def flights():
    if request.method == "POST":
        # Insert
        if request.form.get("AddFlight"):
            airline = request.form["airline"]
            departing = request.form["departing"]
            destination = request.form["destination"]
            departTime = request.form["departTime"]
            arriveTime = request.form["arriveTime"]

            query = """
            INSERT INTO Flights (airline, departing, destination, departTime, arriveTime)
            VALUES (%s, %s, %s, %s, %s)
            """
            cur = mysql.connection.cursor()
            cur.execute(query, (airline, departing, destination, departTime, arriveTime))
            mysql.connection.commit()

            return redirect("/flights")
        
        # Update
        if request.form.get("UpdateFlight"):
            airline = request.form["airline"]
            departing = request.form["departing"]
            destination = request.form["destination"]
            departTime = request.form["departTime"]
            arriveTime = request.form["arriveTime"]
            flightID = request.form["flightID"]

            query = """
            UPDATE Flights
            SET airline = %s, departing = %s, destination = %s,
                departTime = %s, arriveTime = %s
            WHERE flightID = %s
            """
            cur = mysql.connection.cursor()
            cur.execute(query, (airline, departing, destination, departTime, arriveTime, flightID))
            mysql.connection.commit()

            return redirect("/flights")
        
        # Delete
        if request.form.get("DeleteFlight"):
            flightID = request.form["flightID"]

            query = "DELETE FROM Flights WHERE flightID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (flightID,))
            mysql.connection.commit()

            return redirect("/flights")

    # Read
    if request.method == "GET":
        # Get all flights
        query = """
        SELECT flightID AS "Flight ID", airline AS "Airline", departing AS "Departing", destination AS "Destination", DATE_FORMAT(departTime, "%Y-%m-%d %H:%i:%s") AS "Depart Time", DATE_FORMAT(arriveTime,"%Y-%m-%d %H:%i:%s") AS "Arrive Time"
        FROM Flights
        """
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = reserved(cur.fetchall())

    return render_template("flights.j2", data=data)


# Accommodations Entity
    # Citation for the following POST/GET methods:
    # Date: 12/9/2023
    # Based on: [redacted]
    # Source URL: [redacted]
    # With the exception of query code, conditionals, and specifics such as variable names, etc. 
@app.route('/accommodations', methods=["POST", "GET"])
def accommodations():
    if request.method == "POST":
        # Insert 
        if request.form.get("AddAccommodation"):
            propertyName = request.form["propertyName"]
            propertyAddress = request.form["propertyAddress"]
            propertyPhone = request.form["propertyPhone"]
            propertyEmail = request.form["propertyEmail"]
            checkInDate = request.form["checkInDate"]
            checkOutDate = request.form["checkOutDate"]

            # Take into account blank responses for optional fields, set as null
            if not propertyName or propertyName == 'None':
                propertyName = None

            if not propertyPhone or propertyPhone == 'None':
                propertyPhone = None

            query = """
            INSERT INTO Accommodations (propertyName, propertyAddress, propertyPhone, propertyEmail, checkInDate, checkOutDate)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cur = mysql.connection.cursor()
            cur.execute(query, (propertyName, propertyAddress, propertyPhone, propertyEmail, checkInDate, checkOutDate))
            mysql.connection.commit()

            return redirect("/accommodations")
        
        # Update
        if request.form.get("UpdateAccommodation"):
            propertyName = request.form["propertyName"]
            propertyAddress = request.form["propertyAddress"]
            propertyPhone = request.form["propertyPhone"]
            propertyEmail = request.form["propertyEmail"]
            checkInDate = request.form["checkInDate"]
            checkOutDate = request.form["checkOutDate"]
            stayID = request.form["stayID"]

            # Take into account blank responses for optional fields, set as null
            if not propertyName or propertyName == 'None':
                propertyName = None

            if not propertyPhone or propertyPhone == 'None':
                propertyPhone = None

            query = """
            UPDATE Accommodations
            SET propertyName = %s, propertyAddress = %s, propertyPhone = %s,
                propertyEmail = %s, checkInDate = %s, checkOutDate = %s
            WHERE stayID = %s
            """
            cur = mysql.connection.cursor()
            cur.execute(query, (propertyName, propertyAddress, propertyPhone, propertyEmail, checkInDate, checkOutDate, stayID))
            mysql.connection.commit()

            return redirect("/accommodations")
        
        # Delete
        if request.form.get("DeleteAccommodation"):
            stayID = request.form["stayID"]

            query = "DELETE FROM Accommodations WHERE stayID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (stayID,))
            mysql.connection.commit()

            return redirect("/accommodations")

    # Read
    if request.method == "GET":
        # Get all Accommodations
        query = """
        SELECT stayID AS "Stay ID", COALESCE(propertyName, "None") AS "Name", propertyAddress AS "Address", COALESCE(propertyPhone, "None") AS "Phone", propertyEmail AS "Email", DATE_FORMAT(checkInDate, "%Y-%m-%d")  AS "Check-In Date", DATE_FORMAT(checkOutDate, "%Y-%m-%d") AS "Check-Out Date"
        FROM Accommodations
        """
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = reserved(cur.fetchall())

    return render_template("accommodations.j2", data=data)


# Activities Entity 
    # Citation for the following POST/GET methods:
    # Date: 11/16/2023
    # Based on: [redacted]
    # Source URL: [redacted] 
    # With the exception of query code and specifics such as variable names, etc. 

@app.route('/activities', methods=["POST", "GET"])
def activities():
    if request.method == "POST":
        # Insert
        if request.form.get("AddActivity"):
            activityName = request.form["activityName"]
            activityDescription = request.form["activityDescription"]
            activityLocation = request.form["activityLocation"]

            query = "INSERT INTO Activities (activityName, activityDescription, activityLocation) VALUES (%s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (activityName, activityDescription, activityLocation))
            mysql.connection.commit()

            return redirect("/activities")
        
        # Update
        if request.form.get("UpdateActivity"):
            activityName = request.form["activityName"]
            activityDescription = request.form["activityDescription"]
            activityLocation = request.form["activityLocation"]
            activityID = request.form["activityID"]

            query = "UPDATE Activities SET activityName = %s, activityDescription = %s, activityLocation = %s WHERE activityID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (activityName, activityDescription, activityLocation, activityID))
            mysql.connection.commit()

            return redirect("/activities")
        
        # Delete
        if request.form.get("DeleteActivity"):
            activityID = request.form["activityID"]

            query = "DELETE FROM Activities WHERE activityID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (activityID,))
            mysql.connection.commit()

            return redirect("/activities")
        
    # Read
    if request.method == "GET":
        # Get all activities
        query = "SELECT activityID AS 'Activity ID', activityName AS 'Name', activityDescription AS 'Description', activityLocation as 'Location' FROM Activities"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = reserved(cur.fetchall())

    return render_template("activities.j2", data=data)


# ActivitiesRatings Entity 
    # Citation for the following POST/GET methods:
    # Date: 11/16/2023
    # Based on: [redacted]
    # Source URL: [redacted] 
    # With the exception of query code and specifics such as variable names, etc. 

@app.route('/activity-ratings', methods=["GET", "POST"])
def activity_ratings():
    if request.method == "POST":
        # Insert 
        if request.form.get("InsertActivityRating"):
            activityID = request.form["activityID"]
            travelerID = request.form["travelerID"]
            rating = request.form["rating"]
            review = request.form["review"]

            # convert passed binary bool to True/False
            if rating == "1":
                rating = True
            else:
                rating = False

            query = """
            INSERT INTO ActivityRatings (activityID, travelerID, rating, review) 
            VALUES (%s, %s, %s, %s)
            """

            cur = mysql.connection.cursor()
            cur.execute(query, (activityID, travelerID, rating, review))
            mysql.connection.commit()

            return redirect("/activity-ratings")
        
        # Update
        if request.form.get("UpdateActivityRating"):
            activityID = request.form["activityID"]
            travelerID = request.form["travelerID"]
            rating = request.form["rating"]
            review = request.form["review"]
            ratingID = request.form["ratingID"]

            query = """
            UPDATE ActivityRatings
            SET
                activityID = %s,
                travelerID = %s, 
                rating = %s,
                review = %s
            WHERE ratingID = %s
            """
            cur = mysql.connection.cursor()
            cur.execute(query, (activityID, travelerID, rating, review, ratingID))
            mysql.connection.commit()

            return redirect("/activity-ratings")
        
        # Delete
        if request.form.get("DeleteActivityRating"):
            ratingID = request.form["ratingID"]

            query = "DELETE FROM ActivityRatings WHERE ratingID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (ratingID,))
            mysql.connection.commit()

            return redirect("/activity-ratings")
        
    # Read
    if request.method == "GET":
        # Get all Activity Ratings
        query = """
        SELECT
            ActivityRatings.ratingID AS 'Rating ID',

            ActivityRatings.activityID AS 'Activity ID',
            Activities.activityName AS 'Activity Name',

            ActivityRatings.travelerID AS 'Traveler ID',
            Travelers.name AS 'Traveler Name',

            ActivityRatings.rating AS 'Rating',
            ActivityRatings.review AS 'Review'
        FROM ActivityRatings
        JOIN Activities ON Activities.activityID = ActivityRatings.activityID
        JOIN Travelers ON Travelers.travelerID = ActivityRatings.travelerID
        """
        
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = reserved(cur.fetchall())
  
        # Get dropdown for Activities
        query1 = """
        SELECT 
            activityID,
            activityName
        FROM Activities
        """
        cur = mysql.connection.cursor()
        cur.execute(query1)
        activitytData = cur.fetchall()

        # Get dropdown for Travelers
        query3 = "SELECT travelerID, name FROM Travelers"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        travelerData = reserved(cur.fetchall())


    return render_template("activity-ratings.j2", data=data, activitytData=activitytData, travelerData=travelerData)



# Activities - Itineraries Intersection Table

    # Citation for the following POST/GET methods:
    # Date: 12/9/2023
    # Based on: [redacted]
    # Source URL: [redacted]
    # With the exception of query code and specifics such as variable names, etc. 
@app.route('/activities-itineraries', methods=["POST", "GET"])
def activities_itineraries():
    if request.method == "POST":
        # Insert
        if request.form.get("AddActivityItinerary"):
            planID = request.form["planID"]
            activityID = request.form["activityID"]

            query = "INSERT INTO Activities_Itineraries (planID, activityID) VALUES (%s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (planID, activityID))
            mysql.connection.commit()

            return redirect("/activities-itineraries")
        
        # Update
        if request.form.get("UpdateActivityItinerary"):
            planID = request.form["planID"]
            activityID = request.form["activityID"]
            activityItineraryID = request.form["activityItineraryID"]

            query = "UPDATE Activities_Itineraries SET planID = %s, activityID = %s WHERE activityItineraryID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (planID, activityID, activityItineraryID))
            mysql.connection.commit()

            return redirect("/activities-itineraries")
        
        # Delete
        if request.form.get("DeleteActivityItinerary"):
            activityItineraryID = request.form["activityItineraryID"]

            query = "DELETE FROM Activities_Itineraries WHERE activityItineraryID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (activityItineraryID,))
            mysql.connection.commit()

            return redirect("/activities-itineraries")

    # Read
    if request.method == "GET":
        # Get all activities-itineraries
        query = """
        SELECT Activities_Itineraries.activityItineraryID AS 'Activities - Itineraries ID', 
            CONCAT(Itineraries.home, " to ", Itineraries.destination) AS 'Itinerary',
            Activities.activityName AS 'Activity'
        FROM Activities_Itineraries
        JOIN Itineraries ON Activities_Itineraries.planID = Itineraries.planID
        JOIN Activities ON Activities_Itineraries.activityID = Activities.activityID
        ORDER BY Activities_Itineraries.activityItineraryID ASC
        """
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = reserved(cur.fetchall())

        # Get dropdown for Itineraries
        query1 = """
        SELECT 
            planID,
            CONCAT(home, " to ", destination) AS 'Itinerary'
        FROM Itineraries
        """
        cur = mysql.connection.cursor()
        cur.execute(query1)
        itineraryData = reserved(cur.fetchall())

        # Get dropdown for Activities
        query2 = """
        SELECT 
            activityID,
            activityName AS Activity
        FROM Activities
        """
        cur = mysql.connection.cursor()
        cur.execute(query2)
        activityData = reserved(cur.fetchall())

    return render_template("activities-itineraries.j2", data=data, itineraryData=itineraryData, activityData=activityData)
    


# Travelers - Itineraries Intersection Table

    # Citation for the following POST/GET methods:
    # Date: 12/9/2023
    # Based on:[redacted]
    # Source URL:[redacted]
    # With the exception of query code and specifics such as variable names, etc. 
@app.route('/travelers-itineraries', methods=["POST", "GET"])
def travelers_itineraries():
    if request.method == "POST":
        # Insert
        if request.form.get("AddTravelerItinerary"):
            planID = request.form["planID"]
            travelerID = request.form["travelerID"]

            query = "INSERT INTO Travelers_Itineraries (planID, travelerID) VALUES (%s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (planID, travelerID))
            mysql.connection.commit()

            return redirect("/travelers-itineraries")
        
        # Update
        if request.form.get("UpdateTravelerItinerary"):
            planID = request.form["planID"]
            travelerID = request.form["travelerID"]
            travelerItineraryID = request.form["travelerItineraryID"]

            query = "UPDATE Travelers_Itineraries SET planID = %s, travelerID = %s WHERE travelerItineraryID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (planID, travelerID, travelerItineraryID))
            mysql.connection.commit()

            return redirect("/travelers-itineraries")
        
        # Delete
        if request.form.get("DeleteTravelerItinerary"):
            travelerItineraryID = request.form["travelerItineraryID"]

            query = "DELETE FROM Travelers_Itineraries WHERE travelerItineraryID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (travelerItineraryID,))
            mysql.connection.commit()

            return redirect("/travelers-itineraries")

    # Read
    if request.method == "GET":
        # Get all Travelers-Itineraries
        query = """
        SELECT Travelers_Itineraries.travelerItineraryID AS 'Travelers - Itineraries ID', 
            CONCAT(Itineraries.home, " to ", Itineraries.destination) AS 'Itinerary',
            Travelers.name AS 'Traveler'
        FROM Travelers_Itineraries
        JOIN Itineraries ON Travelers_Itineraries.planID = Itineraries.planID
        JOIN Travelers ON Travelers_Itineraries.travelerID = Travelers.travelerID
        ORDER BY Travelers_Itineraries.travelerItineraryID ASC
        """
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = reserved(cur.fetchall())

        # Get dropdown for Itineraries
        query1 = """
        SELECT 
            planID,
            CONCAT(home, " to ", destination) AS 'Itinerary'
        FROM Itineraries
        """
        cur = mysql.connection.cursor()
        cur.execute(query1)
        itineraryData = reserved(cur.fetchall())

        # Get dropdown for Travelers
        query2 = """
        SELECT 
            travelerID,
            name AS Traveler
        FROM Travelers
        """
        cur = mysql.connection.cursor()
        cur.execute(query2)
        travelerData = reserved(cur.fetchall())

    return render_template("travelers-itineraries.j2", data=data, itineraryData=itineraryData, travelerData=travelerData)
    

@app.route('/about-page')
def about_page():
    return render_template("about-page.j2")


@app.route('/unfinished-page')
def unfinished_page():
    return render_template("unfinished-page.j2")


# Listener
if __name__ == "__main__":

    #Start the app on port [redacted], it will be different once hosted
    app.run(port=[redacted], debug=True)
