/*
Dylan Majewski
Tommy Nguyen
*/

SET FOREIGN_KEY_CHECKS = 0;
SET AUTOCOMMIT = 0;

/*
    This file is contains the Data Definition Queries for TripQuick.
There are six entities with 2 intersection tables. The intersection tables is to 
facilitate the M:N relationship between Travelers and Itineraries entities and the
Activities and Itineraries entities. 

This file also contains the sample data for TripQuick.

The data provided are all fake and is not intended to imitate any real person. 
*/

-- Entities

CREATE OR REPLACE TABLE Travelers (
    travelerID int NOT NULL AUTO_INCREMENT,
    name varchar(255) NOT NULL,
    email varchar(255) NOT NULL,
    phone varchar(255) NOT NULL,
    PRIMARY KEY (travelerID)
);

CREATE OR REPLACE TABLE Flights (
    flightID int NOT NULL AUTO_INCREMENT,
    airline varchar(255) NOT NULL,
    departing varchar(255) NOT NULL,
    destination varchar(255) NOT NULL,
    departTime datetime NOT NULL,
    arriveTime datetime NOT NULL,
    PRIMARY KEY (flightID)
);

CREATE OR REPLACE TABLE Accommodations (
    stayID int NOT NULL AUTO_INCREMENT,
    propertyName varchar(255),
    propertyAddress varchar(255) NOT NULL,
    propertyPhone varchar(255),
    propertyEmail varchar(255),
    checkInDate datetime NOT NULL,
    checkOutDate datetime NOT NULL,
    PRIMARY KEY (stayID)
);

CREATE OR REPLACE TABLE Itineraries (
    planID int NOT NULL AUTO_INCREMENT,
    departureFlightID int,
    returnFlightID int,
    stayID int,
    home varchar(255) NOT NULL,
    destination varchar(255) NOT NULL,
    PRIMARY KEY (planID),
    FOREIGN KEY (departureFlightID) REFERENCES Flights (flightID)
    ON DELETE SET NULL,
    FOREIGN KEY (returnFlightID) REFERENCES Flights (flightID)
    ON DELETE SET NULL,
    FOREIGN KEY (stayID) REFERENCES Accommodations (stayID)
    ON DELETE SET NULL
);

CREATE OR REPLACE TABLE Activities (
    activityID int NOT NULL AUTO_INCREMENT,
    activityName varchar(255) NOT NULL,
    activityDescription varchar(255),
    activityLocation varchar(255) NOT NULL,
    PRIMARY KEY (activityID)
);

CREATE OR REPLACE TABLE ActivityRatings (
    ratingID int NOT NULL AUTO_INCREMENT,
    activityID int NOT NULL,
    travelerID int NOT NULL,
    rating boolean NOT NULL,
    review varchar(255),
    PRIMARY KEY (ratingID),
    FOREIGN KEY (activityID) REFERENCES Activities(activityID)
    ON DELETE CASCADE,
    FOREIGN KEY (travelerID) REFERENCES Travelers(travelerID)
    ON DELETE CASCADE
);

-- Intersection Tables

CREATE OR REPLACE TABLE Travelers_Itineraries (
    travelerItineraryID int NOT NULL AUTO_INCREMENT,
    travelerID int,
    planID int,
    PRIMARY KEY (travelerItineraryID),
    FOREIGN KEY (travelerID) REFERENCES Travelers(travelerID)
    ON DELETE CASCADE,
    FOREIGN KEY (planID) REFERENCES Itineraries(planID)
    ON DELETE SET NULL
);

CREATE OR REPLACE TABLE Activities_Itineraries (
    activityItineraryID int NOT NULL AUTO_INCREMENT,
    planID int,
    activityID int,
    PRIMARY KEY (activityItineraryID),
    FOREIGN KEY (planID) REFERENCES Itineraries(planID)
    ON DELETE SET NULL,
    FOREIGN KEY (activityID) REFERENCES Activities(activityID)
    ON DELETE SET NULL
);

-- Example Data

INSERT INTO Travelers (
    travelerID,
    name,
    email,
    phone
) VALUES (
    1,
    "Pauline R. Gibson",
    "shanie1989@hotmail.com",
    "917-204-3621"
),
(
    2,
    "Andrew N. Jones",
    "gillian2002@hotmail.com",
    "832-277-9715"
),
(
    3,
    "Aaron M. Sandoval",
    "louisa2012@yahoo.com",
    "732-644-0435"
),
(
    4,
    "Helen K. White",
    "twila.toy19@hotmail.com",
    "269-416-6835"
),
(
    5,
    "Gail M. Castillo",
    "emelie.steh3@yahoo.com",
    "217-246-6331"
);

INSERT INTO Flights (
    flightID,
    airline,
    departing,
    destination,
    departTime,
    arriveTime
) VALUES (
    1, 
    "Alaska",
    "SEA",
    "LAX",
    "2023-11-11 05:15:00",
    "2023-11-11 08:15:00"
),
(
    2,
    "Delta",
    "BUR",
    "BFI",
    "2023-11-16 12:30:00",
    "2023-11-16 15:30:00"
),
(
    3,
    "United",
    "ONT",
    "PAE",
    "2023-11-04 07:00:00",
    "2023-11-04 11:00:00"
),
(
    4,
    "Southwest",
    "BLI",
    "SAN",
    "2023-10-25 15:00:00",
    "2023-10-25 20:00:00"
);

INSERT INTO Accommodations (
    stayID,
    propertyName,
    propertyAddress,
    propertyPhone,
    propertyEmail,
    checkInDate,
    checkOutDate
) VALUES (
    1,
    "Holiday Inn",
    "453 Rainbow Road, Los Angeles, California(CA), 90014",
    "626-271-4464",
    "rainbow@holidayinn.com",
    "2023-11-11",
    "2023-11-16"
),
(
    2,
    NULL,
    "4520 Joy Lane, Everett, Washington(WA), 98201",
    NULL,
    "camilla@airbnb.com",
    "2023-11-04",
    "2023-11-11"
),
(
    3,
    "Motel 6",
    "4175 Zimmerman Lane, Los Angeles, California(CA), 90017",
    "213-542-7860",
    "manager@motel6.com",
    "2023-10-25",
    "2023-11-16"
);

INSERT INTO Itineraries (
    planID,
    departureFlightID,
    returnFlightID,
    stayID,
    home,
    destination
) VALUES (
    1,
    1,
    2,
    1,
    "Seattle",
    "Los Angeles"
),
(
    2,
    3,
    1,
    2,
    "Anaheim",
    "Everett"
),
(
    3,
    4,
    2,
    3,
    "Tacoma",
    "San Bernardino"
);

INSERT INTO Activities (
    activityID,
    activityName,
    activityDescription,
    activityLocation
) VALUES (
    1,
    "The Celestial Observatory Tower",
    "This observatory allows visitors to explore the cosmos and observe celestial objects through state-of-the-art telescopes. Guests can attend engaging astronomy shows, stargazing events, and even participate in guided tours.",
    "Los Angeles, CA"
),
(
    2,
    "Urban Legends Mystery House",
    "This house is filled with rooms and passages that challenge your perceptions and boggle your mind. Explore optical illusions, solve puzzles, and uncover the secrets hidden within its walls.",
    "Los Angeles, CA"
),
(
    3,
    "Whale Watcher's Haven",
    "Whale Watcher's Haven is a coastal sanctuary where visitors can embark on thrilling whale-watching expeditions. Climb aboard state-of-the-art vessels to witness majestic orcas, humpback whales, and other marine life in their natural habitat.",
    "Everett, WA"
);

INSERT INTO ActivityRatings (
    ratingID,
    activityID,
    travelerID,
    rating,
    review
) VALUES (
    1,
    1,
    4,
    TRUE,
    "The shows were amazing and spectacular! You can really tell that a lot of thought and effort was put into this place. The employees here are very passionate about their jobs as well which makes it all a very enjoyable experience!"
),
(
    2,
    2,
    5,
    TRUE,
    "It was very intriguting and challenging but that's part of the fun! Definitely come here if you want some mental stimulation!"
),
(
    3,
    2,
    3,
    FALSE,
    "It was too confusing, and difficult and I could not figure anything out."
),
(
    4,
    3,
    1,
    TRUE,
    "Whale Watcher's Haven is a dream come true! Saw orcas up close, and it left me speechless. Unforgettable experience. A must-visit!"
),
(
    5,
    3,
    2,
    TRUE,
    "We spotted humpback whales and dolphins. The crew was fantastic. Highly recommended for nature lovers."
);

INSERT INTO Activities_Itineraries (
    activityItineraryID,
    planID,
    activityID
) VALUES (
    1,
    1,
    1
),
(
    2,
    3,
    1
),
(
    3,
    3,
    2
),
(
    4,
    2,
    3
);

INSERT INTO Travelers_Itineraries (
    travelerItineraryID,
    planID,
    travelerID
) VALUES (
    1,
    1,
    1
),
(
    2,
    1,
    2
),
(
    3,
    2,
    3
),
(
    4,
    3,
    4
);


SET FOREIGN_KEY_CHECKS = 0;
COMMIT;
