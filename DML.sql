/*
Dylan Majewski
Tommy Nguyen
*/

SET FOREIGN_KEY_CHECKS = 0;
SET AUTOCOMMIT = 0;


-- This file contains a list of queries made for TripQuick.


/*
!!!!!
THROUGHOUT THIS QUERY CONTAINS VARIABLES THAT ARE DENOTED BY A COLON : CHARACTER
THAT WILL BE REPLACED WITH DATA FROM THE BACKEND PROGRAMMING LANGUAGE WHEN IMPLEMENTED.

NOT ALL QUERIES LISTED BELOW WERE USED IN TRIPQUICK. 
HOWEVER, ALL QUERIES THAT WERE USED ARE BELOW.

ALSO, SOME QUERIES ARE TRIPQUICK APP.PY SPECIFIC, AS IN, IT USES LOCAL VARIABLES WHICH
ARE SPECIFIED IN THE APP.PY FILE. 

THIS FILE IS NOT INTENDED TO BE EXECUTED. 
IT SIMPLY ACTS AS A MASTER LIST OF THE QUERIES USED AND ADDITIONAL POTENTIAL QUERIES.
!!!!!
*/



/*
    Read/show data for all attributes of an entity
*/

-- Get all travelers
SELECT * FROM Travelers;

-- Get all intineraries
SELECT * FROM Itineraries;

-- Get all flights
SELECT * FROM Flights;

-- Get all accommodations
SELECT * FROM Accommodations;

-- Get all activites
SELECT * FROM Activities;

-- Get all ratings
SELECT * FROM ActivityRatings;

/*
    IMPLEMENTED AS ALIASES 
*/

-- Get all travelers
SELECT travelerID AS "Traveler ID", name AS "Name", email AS "Email address", phone as "Phone number"
FROM Travelers;

-- Get all itineraries
SELECT Itineraries.planID AS 'Itinerary ID', 
    COALESCE(CONCAT(DepartureFlights.departing, ' to ', DepartureFlights.destination), 'None') AS 'Departure Ticket', 
    COALESCE(CONCAT(ReturnFlights.departing, ' to ', ReturnFlights.destination), 'None') AS 'Return Ticket', 
    COALESCE(Accommodations.propertyName, Accommodations.propertyAddress, 'None') AS 'Accommodation',
    Itineraries.home AS 'Home', 
    Itineraries.destination AS 'Destination' 
FROM Itineraries
LEFT JOIN Flights AS DepartureFlights ON DepartureFlights.flightID = Itineraries.departureFlightID 
LEFT JOIN Flights AS ReturnFlights ON ReturnFlights.flightID = Itineraries.returnFlightID 
LEFT JOIN Accommodations ON Accommodations.stayID = Itineraries.stayID;

-- Get all flights with date reformatting 
SELECT flightID AS "Flight ID", airline AS "Airline", departing AS "Departing", destination AS "Destination", DATE_FORMAT(departTime, "%Y-%m-%d %H:%i:%s") AS "Depart Time", DATE_FORMAT(arriveTime,"%Y-%m-%d %H:%i:%s") AS "Arrive Time"
FROM Flights;

-- Get all accommodations with date reformatting and null handling 
SELECT stayID AS "Stay ID", COALESCE(propertyName, "None") AS "Name", propertyAddress AS "Address", COALESCE(propertyPhone, "None") AS "Phone", propertyEmail AS "Email", DATE_FORMAT(checkInDate, "%Y-%m-%d")  AS "Check-In Date", DATE_FORMAT(checkOutDate, "%Y-%m-%d") AS "Check-Out Date"
FROM Accommodations;

-- Get all activities
SELECT activityID AS "Activity ID", activityName AS "Name", activityDescription AS "Description", activityLocation AS "Location"
FROM Activities;

--  Get all ratings
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
JOIN Travelers ON Travelers.travelerID = ActivityRatings.travelerID;



/*
    Read/show data for intersection tables
*/

-- Get all Activities_Itineraries
SELECT * 
FROM Activities_Itineraries;

-- Get all Travelers_Itineraries
SELECT * 
FROM Travelers_Itineraries;

/*
    Read/show data for intersection tables with AS Aliases 
*/

-- Get all Activities_Itineraries
SELECT Activities_Itineraries.activityItineraryID AS 'Activities - Itineraries ID', 
    CONCAT(Itineraries.home, " to ", Itineraries.destination) AS 'Itinerary',
    Activities.activityName AS 'Activity'
FROM Activities_Itineraries
JOIN Itineraries ON Activities_Itineraries.planID = Itineraries.planID
JOIN Activities ON Activities_Itineraries.activityID = Activities.activityID
ORDER BY Activities_Itineraries.activityItineraryID ASC;

-- Get all Travelers_Itineraries
SELECT Travelers_Itineraries.travelerItineraryID AS 'Travelers - Itineraries ID', 
    CONCAT(Itineraries.home, " to ", Itineraries.destination) AS 'Itinerary',
    Travelers.name AS 'Traveler'
FROM Travelers_Itineraries
JOIN Itineraries ON Travelers_Itineraries.planID = Itineraries.planID
JOIN Travelers ON Travelers_Itineraries.activityID = Travelers.travelerID
ORDER BY Travelers_Itineraries.travelerItineraryID ASC;



/*
    Read/show data for dropdown menu (Search/filter) | Dynamically populated lists
*/

-- Get list of Travelers by name
SELECT
    travelerID,
    name
FROM Travelers;

-- Get list of Travelers by name AS ALIASES specific
SELECT 
    travelerID, 
    name AS Traveler
FROM Travelers;

-- Get list of Itineraries by home and destination
SELECT 
    planID,
    CONCAT(home, " to ", destination) AS 'Itinerary',
FROM Itineraries;

-- Get list of Activities by name
SELECT
    activityID,
    activityName
FROM Activities;

-- Get list of Activities by ID and name AS ALIASES specific
SELECT 
    activityID,
    activityName AS Activity
FROM Activities;

-- Get list of Accommodations by name/address
SELECT
    stayID,
    CASE
        WHEN Accommodations.propertyName IS NULL THEN Accommodations.propertyAddress
        ELSE Accommodations.propertyName
    END AS 'Accommodations'
FROM Accommodations;

-- Get list of Flights by airline and destination
SELECT 
    flightID,
    CONCAT(departing, ' to ', destination) AS "Flights"
FROM Flights;

-- Get list of ActivityRatings rating options
SELECT ActivityRatings.rating 
FROM ActivityRatings
GROUP BY ActivityRatings.rating;



/*
    Read/show data with a more specific purpose (e.g. searches) for future use
*/

-- Get all travelers and their itineraries 
SELECT Travelers.travelerID, Travelers.name, Itineraries.planID
FROM Travelers
LEFT JOIN Travelers_Itineraries ON Travelers.travelerID = Travelers_Itineraries.travelerID
LEFT JOIN Itineraries ON Travelers_Itineraries.planID = Itineraries.planID
ORDER BY Travelers.travelerID;

-- Get a traveler's list of itineraries and its details based on ID
SELECT * 
FROM Itineraries
JOIN Travelers_Itineraries ON Itineraries.planID = Travelers_Itineraries.planID
JOIN Travelers ON Travelers_Itineraries.travelerID = Travelers.travelerID AND Travelers.travelerID = :travelerIDInput
ORDER BY Itineraries.planID;

-- Get a traveler's list of itineraries and its details based on name 
SELECT * 
FROM Itineraries
JOIN Travelers_Itineraries ON Itineraries.planID = Travelers_Itineraries.planID
JOIN Travelers ON Travelers_Itineraries.travelerID = Travelers.travelerID AND Travelers.name = :nameInput
ORDER BY Itineraries.planID;

-- Get all itineraries and the travelers associated with them
SELECT * 
FROM Itineraries
JOIN Travelers_Itineraries ON Itineraries.planID = Travelers_Itineraries.planID
JOIN Travelers ON Travelers_Itineraries.travelerID = Travelers.travelerID
ORDER BY Itineraries.planID;

-- Get departure flight details for specified itinerary
SELECT Itineraries.planID, Flights.flightID, Flights.airline, Flights.departing, Flights.destination, Flights.departTime, Flights.arriveTime
FROM Flights
JOIN Itineraries ON Itineraries.departureFlightID = Flights.flightID AND Itineraries.planID = :planIDInput;

-- Get return flight details for specified itinerary
SELECT Itineraries.planID, Flights.flightID, Flights.airline, Flights.departing, Flights.destination, Flights.departTime, Flights.arriveTime
FROM Flights
JOIN Itineraries ON Itineraries.returnFlightID = Flights.flightID AND Itineraries.planID = :planIDInput;

-- Get accommodation details for a specified itinerary
SELECT Itineraries.planID, ACC.stayID, ACC.propertyName, ACC.propertyPhone, ACC.propertyEmail, ACC.checkInDate, ACC.checkOutDate
FROM Accommodations AS ACC
JOIN Itineraries ON Itineraries.stayID = ACC.stayID AND Itineraries.planID = :planIDInput;

-- Get all activities tied to a itinerary
SELECT Itineraries.planID, ACT.activityID, ACT.activityName, ACT.activityLocation
FROM Activities AS ACT
JOIN Activities_Itineraries ON ACT.activityID = Activities_Itineraries.activityID
JOIN Itineraries ON Activities_Itineraries.planID = Itineraries.planID AND Itineraries.planID = :planIDInput
ORDER BY ACT.activityID;

-- Get all ratings from a traveler
SELECT Travelers.name, ActivityRatings.ratingID, Activities.activityName, ActivityRatings.rating, ActivityRatings.review
FROM ActivityRatings
JOIN Travelers ON Travelers.travelerID = ActivityRatings.travelerID 
JOIN Activities ON Activities.activityID = ActivityRatings.activityID AND ActivityRatings.travelerID = :travelerIDInput
ORDER BY ActivityRatings.activityID;

-- Get all ratings for an activity
SELECT ActivityRatings.ratingID, Travelers.name, Activities.activityName, ActivityRatings.rating, ActivityRatings.review
FROM ActivityRatings
JOIN Travelers ON Travelers.travelerID = ActivityRatings.travelerID 
JOIN Activities ON Activities.activityID = ActivityRatings.activityID AND ActivityRatings.activityID = :activityIDInput
ORDER BY ActivityRatings.activityID;



/*
    Entities Creations
*/

-- Add new traveler
INSERT INTO Travelers (name, email, phone) 
VALUES (:nameInput, :emailInput, :phoneInput);

-- Add itinerary
INSERT INTO Itineraries (departureFlightID, returnFlightID, stayID, home, destination)
VALUES (:departureFlightIDInput, :returnFlightIDInput, :stayIDInput, :homeInput, :destinationInput);

-- Add itinerary by use of tuple        !!! APP.PY SPECIFIC
INSERT INTO Itineraries (departureFlightID, returnFlightID, stayID, home, destination) 
VALUES (" + ", ".join(":inputs" if values[key] else "NULL" for key in values.keys()) + ");

-- Add flight
INSERT INTO Flights (airline, departing, destination, departTime, arriveTime)
VALUES (:airlineInput, :departingInput, :destinationInput, :departTimeInput, :arriveTimeInput);

-- Add accommodation
INSERT INTO Accommodations (propertyName, propertyAddress, propertyPhone, propertyEmail, checkInDate, checkOutDate)
VALUES (:propertyNameInput, :propertyAddressInput, :propertyPhoneInput, :propertyEmailInput, :checkInDateInput, :checkOutDateInput);

-- Add activity
INSERT INTO Activities (activityName, activityDescription, activityLocation)
VALUES (:activityNameInput, :activityDescriptionInput, :activityLocationInput);

-- Add rating
INSERT INTO ActivityRatings (activityID, travelerID, rating, review)
VALUES (:activityIDInput, :travelerIDInput, :ratingInput, :reviewInput);



/*
    Intersection Table Creations
*/

-- Add traveler to itinerary (M:N) addition
INSERT INTO Travelers_Itineraries (travelerID, planID)
VALUES (:travelerIDInput, :planIDInput);

-- Add activity to itinerary (M:N) addition
INSERT INTO Activities_Itineraries (planID, activityID)
VALUES (:planIDInput, :activityIDInput);



/*
    Entities Updates
*/

-- Update a traveler's personal information
UPDATE Travelers 
SET name = :nameInput, email = :emailInput, phone = :phoneInput
WHERE travelerID = :travelerIDInput;

-- Update itinerary
UPDATE Itineraries
SET departureFlightID = :departureFlightIDInput, returnFlightID = :returnFlightIDInput, 
    stayID = :stayIDInput, home = :homeInput, destination = :destinationInput
WHERE planID = :planIDInput;

-- Update itinerary by use of tuple     !!! APP.PY SPECIFIC
UPDATE Itineraries 
SET " + sub_query + " 
WHERE planID = :planIDInput;

-- Update flight details
UPDATE Flights
SET airline = :airlineInput, departing = :departingInput, destination = :destinationInput,
    departTime = :departTimeInput, arriveTime = :arriveTimeInput
WHERE flightID = :flightIDInput;

-- Update an accommodation
UPDATE Accommodations
SET propertyName = :propertyNameInput, propertyAddress = :propertyAddressInput, propertyPhone = :propertyPhoneInput,
    propertyEmail = :propertyEmailName, checkInDate = :checkInDateInput, checkOutDate = :checkOutDateInput
WHERE stayID = :stayIDInput;

-- Update an activity
UPDATE Activities
SET activityName = :activityNameInput, activityDescription = :activityDescriptionInput, activityLocation = :activityLocationInput
WHERE activityID = :activityIDInput;

-- Update a rating
UPDATE ActivityRatings
SET rating = :ratingInput, review = :reviewInput
WHERE ratingID = :ratingIDInput;



/*
    Intersection Table Updates
*/

-- Update Activities_Itineraries
UPDATE Activities_Itineraries
SET planID = :planIDInput, activityID = :activityIDInput
WHERE activitiesItinerariesID = :activitiesItinerariesIDInput;

-- Update Travelers_Itineraries
UPDATE Travelers_Itineraries 
SET planID = :planIDInput, travelerID = :travelerIDInput
WHERE travelerItineraryID = :travelerItineraryIDInput;



/*
    Entities Deletions
*/

-- Delete a traveler
DELETE FROM Travelers
WHERE travelerID = :travelerIDInput;

-- Delete itinerary
DELETE FROM Itineraries
WHERE planID = :planIDInput;

-- Delete flight
DELETE FROM Flights
WHERE flightID = :flightIDInput;

-- Delete accommodations
DELETE FROM Accommodations
WHERE stayID = :stayIDInput;

-- Delete activity
DELETE FROM Activities
WHERE activityID = :activityIDInput;

-- Delete rating
DELETE FROM ActivityRatings
WHERE ratingID = :ratingIDInput;



/*
    Intersection Table Deletions
*/

-- Removes traveler from itinerary
DELETE FROM Travelers_Itineraries
WHERE travelerItineraryID = :travelerItineraryIDInput;

-- Removes activity from itinerary 
DELETE FROM Activities_Itineraries
WHERE activitiesItinerariesID = :activitiesItinerariesIDInput;




SET FOREIGN_KEY_CHECKS = 0;
COMMIT;
