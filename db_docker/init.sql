-- Active: 1776360909447@@127.0.0.1@3306@NYPD
#Drop the database every time to allow changes
DROP DATABASE IF EXISTS NYPD;
#Create database and use it in the sql file
CREATE DATABASE IF NOT EXISTS NYPD;
USE NYPD;

#Create Entity tables

#Person info table: Stores Driving lincense number and basic personal info
CREATE TABLE IF NOT EXISTS Person(
	DLNum VARCHAR(50) PRIMARY KEY,
    FName VARCHAR(50) NOT NULL,
    LName VARCHAR(50) NOT NULL,
    DOB DATE NOT NULL,
    Height DECIMAL(4,1),
    WEIGHT DECIMAL(5,1),
    EyeColour VARCHAR(50),
    DLState VARCHAR(25) NOT NULL
);

#Vehicle Table: Stores basic info while using the VIN as the primary key
CREATE TABLE IF NOT EXISTS Vehicle(
	VIN VARCHAR(50) PRIMARY KEY,
    LPlate VARCHAR(50) NOT NULL,
    StatePlate VARCHAR(50) NOT NULL,
    Year INT NOT NULL,
    Make VARCHAR(50) NOT NULL
);

#Address table: stores info about someones address
CREATE TABLE IF NOT EXISTS Address(
	Number INT NOT NULL,
    ZipCode VARCHAR(50) NOT NULL,
    Street VARCHAR(50) NOT NULL,
    State VARCHAR (50) NOT NULL,
    PRIMARY KEY (Number, ZipCode)
);

#Notice table - Some basic info about the notice of when and where
CREATE TABLE IF NOT EXISTS Notice(
	NID INT PRIMARY KEY AUTO_INCREMENT,
    Date date NOT NULL,
    Time time NOT NULL,
    Location VARCHAR(50) NOT NULL
);

#Violation code table, some basic violations that may be found
CREATE TABLE IF NOT EXISTS ViolationCode(
	VioCode VARCHAR(50) PRIMARY KEY,
    Description VARCHAR(255) NOT NULL
);

#Inserting some sample data
INSERT INTO ViolationCode(VioCode, Description)
VALUES('Light01', '1 or more headlight is out'),
('Speed01', '5MPH over speed limit'),
('Light02', 'Breaklight out');

#ActionCode table - the actions from the brief
CREATE TABLE IF NOT EXISTS ActionCode(
	ActCode VARCHAR(50) PRIMARY KEY,
    Description VARCHAR(255) NOT NULL
);

#Inserting some sample data
INSERT INTO ActionCode (ActCode, Description)
VALUES ('Warn1', 'This is a warning, no further action is needed'),
('Repair01', 'You need to repair this vehicle immediately'),
('Correct14','You need to correct and return this to a station within 14 days');

# a table for some basic info about the officer
CREATE TABLE IF NOT EXISTS Officer(
	PID INT PRIMARY KEY UNIQUE,
    FName VARCHAR(50) NOT NULL,
    LName VARCHAR(50) NOT NULL
);

#Create Detatchment Table
CREATE TABLE IF NOT EXISTS Detatchment(
	DetachID INT PRIMARY KEY AUTO_INCREMENT,
    DetatchName VARCHAR(50) NOT NULL
);

#Create District Table
CREATE TABLE IF NOT EXISTS District(
	DistrictID INT PRIMARY KEY AUTO_INCREMENT,
    DistrictName VARCHAR(50) NOT NULL
);	

#Create Relationship Tables

#Creates a table to represent: (Person 1 -> Lives -> N Address)
CREATE TABLE IF NOT EXISTS Lives(
	DLNum VARCHAR(50) NOT NULL,
    Number INT NOT NULL,
    ZipCode VARCHAR(50) NOT NULL,
    PRIMARY KEY (DLNum, Number, ZipCode),
    FOREIGN KEY (DLNum) REFERENCES Person(DLNum)
    ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (Number, ZipCode) REFERENCES Address(Number,ZipCode)
    ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Registered(
    Number INT NOT NULL,
    ZipCode VARCHAR(50) NOT NULL,
    VIN VARCHAR(50) NOT NULL,
    PRIMARY KEY(Number, ZipCode, VIN),
    FOREIGN KEY (Number, ZipCode) REFERENCES Address(Number,ZipCode)
    ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (VIN) REFERENCES Vehicle(VIN)
    ON UPDATE CASCADE ON DELETE CASCADE
);

#Creates a table to represent: (Person 1 -> Owns -> N Vehicle)
CREATE TABLE IF NOT EXISTS Owns(
	DLNum VARCHAR(50) NOT NULL,
    VIN VARCHAR(50) NOT NULL,
    PRIMARY KEY(DLNum,VIN),
    FOREIGN KEY(DLNum) REFERENCES Person(DLNum)
    ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (VIN) REFERENCES Vehicle(VIN)
    ON UPDATE CASCADE ON DELETE CASCADE
);

#Creates a table to represent: (Person 1 -> Commits -> N Notice)
CREATE TABLE IF NOT EXISTS Commits(
	DLNum VARCHAR(50) NOT NULL,
    NID INT NOT NULL,
    PRIMARY KEY(DLNum, NID),
    FOREIGN KEY(DLNum) REFERENCES Person(DLNum)
    ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(NID) REFERENCES Notice(NID)
    ON UPDATE CASCADE ON DELETE CASCADE
);

#Creates a table to represent: (Vehicle 1 -> N Notice)
CREATE TABLE IF NOT EXISTS Involves(
	NID INT NOT NULL,
    VIN VARCHAR(50) NOT NULL,
    PRIMARY KEY(NID,VIN),
    FOREIGN KEY(NID) REFERENCES Notice(NID)
    ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(VIN) REFERENCES Vehicle(VIN)
    ON UPDATE CASCADE ON DELETE CASCADE
);

#Creates a table to represent: (Notice N -> Issues -> 1 Officer)
CREATE TABLE IF NOT EXISTS Issues(
	NID INT NOT NULL,
    PID INT NOT NULL,
    PRIMARY KEY (NID, PID),
    FOREIGN KEY(NID) REFERENCES Notice(NID)
    ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(PID) REFERENCES Officer(PID)
    ON UPDATE CASCADE ON DELETE CASCADE
);

#Creates a table to represent: (Notice N -> NoticeVio -> N ViolationCode)
CREATE TABLE IF NOT EXISTS NoticeVio(
	NID INT NOT NULL,
    ItemID INT NOT NULL,
    VioCode VARCHAR(50) NOT NULL,
    Notes VARCHAR(100) NOT NULL,
    PRIMARY KEY(NID, ItemID),
    FOREIGN KEY(NID) REFERENCES Notice(NID)
    ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(VioCode) REFERENCES ViolationCode(VioCode)
);

#Creates a table to represent: (Notice N -> NoticeAction -> N ActionCode)
CREATE TABLE IF NOT EXISTS NoticeAction(
	NID INT NOT NULL PRIMARY KEY,
    ActCode VARCHAR(50) NOT NULL,
    FOREIGN KEY(NID) REFERENCES Notice(NID)
    ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(ActCode) REFERENCES ActionCode(ActCode)
    ON UPDATE CASCADE ON DELETE CASCADE
);

#Creates a table to represent: (Officer N -> Assigned -> 1 Detachment)
CREATE TABLE IF NOT EXISTS Assigned(
	PID INT PRIMARY KEY,
    DetachID INT NOT NULL,
    FOREIGN KEY(PID) REFERENCES Officer(PID)
    ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(DetachID) REFERENCES Detatchment(DetachID)
    ON UPDATE CASCADE ON DELETE CASCADE
);

#Creates a table to represent: (Detachment N -> PartOf -> 1 District)
CREATE TABLE IF NOT EXISTS PartOf(
	DetatchID INT PRIMARY KEY,
    DistrictID INT NOT NULL,
    FOREIGN KEY (DetatchID) REFERENCES Detatchment(DetachID)
    ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (DistrictID) REFERENCES District(DistrictID)
    ON UPDATE CASCADE ON DELETE CASCADE
);


# --------------------------------------
# DCL STATEMENTS
# --------------------------------------


#Create roles


CREATE ROLE IF NOT EXISTS civiRole;
CREATE ROLE IF NOT EXISTS policeRole;



DELIMITER //
#Make a procedure to give access to all data relating to a specific driver
CREATE DEFINER = 'root'@'%'  PROCEDURE GetCiviData(IN dlNum VARCHAR(50)) SQL SECURITY DEFINER
BEGIN
	SELECT p.DLNum, p.FName, p.LName, p.DOB, v.VIN, v.LPlate, n.NID, n.Date AS NoticeDate, n.Time AS NoticeTime, n.Location AS NoticeLocation, vc.VioCode, vc.Description AS ViolationDescription, ac.ActCode, ac.Description AS ActionRequired
	From Person p
    LEFT JOIN Commits c ON p.DLNum = c.DLNum
    LEFT JOIN  Notice n on c.NID = n.NID
    LEFT JOIN NoticeVio nv on n.NID = nv.NID
    LEFT JOIN ViolationCode vc on nv.VioCode = vc.VioCode
    LEFT JOIN NoticeAction na on n.NID = na.NID
    LEFT JOIN ActionCode ac ON na.ActCode = ac.ActCode
    LEFT JOIN Involves inv ON n.NID = inv.NID
    LEFT JOIN Vehicle v on inv.VIN = v.VIN
    WHERE p.DLNum = dlNum
    ORDER BY n.Date DESC;
END //
DELIMITER  ;


#Give civiRole access to GetCiviData Procedure
GRANT EXECUTE ON PROCEDURE NYPD.GetCiviData to civiRole;
GRANT EXECUTE ON PROCEDURE NYPD.GetCiviData to policeRole;

#Create basic civilian Users
CREATE USER IF NOT EXISTS 'JohnSmith'@'%' IDENTIFIED BY 'password';
GRANT civiRole to 'JohnSmith'@'%';
SET DEFAULT ROLE civiRole TO 'JohnSmith'@'%';


#Create Police Officer
CREATE USER IF NOT EXISTS 'PaulAdams'@'%' IDENTIFIED BY 'password';
GRANT policeRole to 'PaulAdams'@'%';
SET DEFAULT ROLE policeRole to 'PaulAdams'@'%';

#Create overall administrator
CREATE USER IF NOT EXISTS 'admin'@'localhost' IDENTIFIED BY 'admin';
GRANT ALL PRIVILEGES ON *.* TO 'admin'@'localhost';


CREATE USER IF NOT EXISTS 'root'@'localhost' IDENTIFIED BY 'root';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost';
flush privileges;

# --------------------------------------
# DML STATEMENTS
# --------------------------------------

DELIMITER //
#written to save time later on 
#Procedure to add a person address and vehicle instead of writing many insert statements
CREATE PROCEDURE AddPersonAddressVehicle(
	#Person info
    IN DLNum VARCHAR(50),
	IN FName VARCHAR(50),
    IN LName VARCHAR(50),
    IN DOB DATE,
    IN Height DECIMAL(4,1),
    IN Weight DECIMAL(5,1),
    IN EyeColour VARCHAR(50),
    IN DLState VARCHAR(25),
    #Address info
    IN Number INT,
    IN ZipCode VARCHAR(50),
    IN Street VARCHAR(50),
    IN State VARCHAR(50),
    #Vehicle info
    IN VIN VARCHAR(50),
    IN LPlate VARCHAR(50),
    IN StatePlate VARCHAR(50),
    IN Year INT,
    IN Make VARCHAR(50)
    )
	BEGIN
		DECLARE EXIT HANDLER FOR SQLEXCEPTION
        BEGIN
			ROLLBACK;
        END;
        START TRANSACTION;
        # Insert into Person Table
        INSERT INTO Person (DLNum, FName, LName, DOB, Height, Weight, EyeColour, DLState)
        VALUES (DLNum, FName, LName, DOB, Height, Weight, EyeColour, DLState);
        #Insert into Address Table
        INSERT IGNORE INTO Address(Number, ZipCode, Street, State)
        VALUES (Number, ZipCode, Street, State);
        #Insert into Vehicle Table
        INSERT INTO Vehicle(VIN, LPlate, StatePlate, Year, Make)
        VALUES (VIN, LPlate, StatePlate, Year, Make);
        #Insert into Lives Relationship Table
        INSERT INTO Lives (DLNum, Number, ZipCode)
        VALUES (DLNum, Number, ZipCode);
        #Insert into Owns Relationship Table
        INSERT INTO Owns (DLNum, VIN)
        VALUES (DLNum,VIN);
        COMMIT;
	END //
DELIMITER ;
GRANT EXECUTE ON PROCEDURE NYPD.AddPersonAddressVehicle TO policeRole;

# Add officer Department District generator
DELIMITER //
CREATE PROCEDURE AddOficerDepartmentDistrict(
	IN districtName VARCHAR(50),
    IN detatchName VARCHAR(50),
    IN pID INT,
    IN fName VARCHAR(50),
    IN lName VARCHAR(50)
)
BEGIN
	DECLARE newDistrictID INT;
    DECLARE newDetatchID INT;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
		ROLLBACK;
    END;
	START TRANSACTION;
    
    INSERT IGNORE INTO District(DistrictName)
    VALUES(districtName);
    SET newDistrictID = LAST_INSERT_ID();
    INSERT IGNORE INTO Detatchment (DetatchName)
    VALUES (detatchName);
    SET newDetatchID = LAST_INSERT_ID();
    INSERT INTO PartOf (DetatchID, DistrictID)
    VALUES(newDetatchID, newDistrictID);
    INSERT INTO Officer (PID, FName, LName)
    VALUES(pID, fName, lName);
    INSERT INTO Assigned(PID, DetachID)
    VALUES(pID, newDetatchID);
    Commit;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE AddDetatchmentDistrict(
    IN districtName VARCHAR(50),
    IN detatchName VARCHAR(50)
)
BEGIN
	DECLARE newDistrictID INT;
    DECLARE newDetatchID INT;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
		ROLLBACK;
    END;
	START TRANSACTION;
    
    INSERT IGNORE INTO District(DistrictName)
    VALUES(districtName);
    SELECT DistrictID INTO newDistrictID FROM District WHERE DistrictName = districtName;
    INSERT IGNORE INTO Detatchment (DetatchName)
    VALUES (detatchName);
    SELECT DetatchID INTO newDetatchID FROM Detatchment WHERE DetatchName = detatchName;
    INSERT INTO PartOf (DetatchID, DistrictID)
    VALUES(newDetatchID, newDistrictID);
    Commit;
END //
DELIMITER ;



# Add new Notice procedure
DELIMITER //
CREATE PROCEDURE addNotice(
	IN date DATE,
    IN time TIME,
    IN location VARCHAR(50),
    IN dLNum VARCHAR(50),
    IN vIN VARCHAR(50),
    IN pID INT,
    IN vioCode VARCHAR(50),
    IN notes VARCHAR(100),
    IN actCode VARCHAR(50)
)

BEGIN
	DECLARE newNoticeID INT;
	DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
		ROLLBACK;
    END;
    
    START TRANSACTION;
    INSERT INTO Notice(Date, Time, Location)
    VALUES (date, time, location);
    SET newNoticeID = LAST_INSERT_ID();
    INSERT INTO Commits (DLNum, NID)
    VALUES(dLNum, newNoticeID);
    INSERT INTO Involves(NID,VIN)
    VALUES(newNoticeID,vIN);
    INSERT INTO Issues(NID,PID)
    VALUES(newNoticeID,pID);
    INSERT INTO NoticeVio(NID, ItemID,VioCode,Notes)
    VALUES(newNoticeID, 1, vioCode, notes);
    INSERT INTO NoticeAction(NID,ActCode)
    VALUES (newNoticeID, actCode);
    COMMIT;
END //
DELIMITER ;
GRANT EXECUTE ON PROCEDURE NYPD.addNotice TO policeRole;

# Insert sample data

#Sample People
CALL AddPersonAddressVehicle('NY123456', 'John', 'Smith','2000-1-1',102.2,50.0,'Blue','NY',  '123', '1001', '5th Ave', 'NY',  'SAMPLE VIN1', 'NY1234', 'NY', 2021, 'Honda Civic');
CALL AddPersonAddressVehicle('NY144567', 'Tim', 'Addams','2004-5-6',134.2,55.0,'Green','NY',  '123', '1001', '5th Ave', 'NY',  'SAMPLE VIN2', 'NY2345', 'NY', 2023, 'BMW M3');
#Sample Officers
CALL AddOficerDepartmentDistrict('Manhattan North', '15th station', 1234, 'Paul','Adams');
CALL AddOficerDepartmentDistrict('Manhattan South', '12th station', 2345, 'Sarah','Jane');
#Sample Notice / Violation
CALL addNotice('2025-10-5', '20:00','13th strt, 5th ave', 'NY123456', 'SAMPLE VIN1', 1234,'Light01','Front-Right headlight is Out','Correct14');
CALL addNotice('2025-10-6', '21:21','13th strt, 5th ave', 'NY123456', 'SAMPLE VIN1', 1234,'Light02','Back left Breaklight is out','Correct14');
CALL addNotice('2025-10-3', '09:32','15th strt, 5th ave', 'NY144567', 'SAMPLE VIN1', 1234,'Light02','Back left Breaklight is out','Correct14');

 
 
SELECT * FROM NoticeVio WHERE NID = 1;
UPDATE NoticeVio SET Notes = 'Front-Left headlight is Out' WHERE NID = 1;
SELECT * FROM NoticeVio WHERE NID = 1;
SELECT * FROM NoticeVio WHERE NID = 2;
UPDATE NoticeVio SET Notes = 'Front-Right headlight is Out', VioCode = 'Light01' WHERE NID = 2;
SELECT * FROM NoticeVio WHERE NID = 2;