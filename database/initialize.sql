USE flights;
DROP TABLE IF EXISTS `users`;

-- users 
CREATE TABLE `users` (
  `User_ID` int NOT NULL AUTO_INCREMENT,
  `User_Name` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL,
  `Creation_Date` datetime DEFAULT NULL,
  `Last_Login` datetime DEFAULT NULL,
  `Password` varchar(100) COLLATE utf8mb3_bin DEFAULT NULL,
  `Email` varchar(100) UNIQUE COLLATE utf8mb3_bin DEFAULT NULL ,
  PRIMARY KEY (`User_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;

INSERT INTO users (User_Name, Creation_Date, Last_Login, Password, Email)
VALUES ('John',CURRENT_TIMESTAMP,NULL,'123','john@gmail.com');

-- Flights 
DROP TABLE IF EXISTS `flights`;
CREATE TABLE `flights` (
  `Flight_ID` int NOT NULL UNIQUE,
  `Departure_City` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL,
  `Arrival_City` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `Departure_Date` datetime DEFAULT NULL,
  `Available_Seats` int DEFAULT NULL,
  `Flight_Company` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  PRIMARY KEY (`Flight_ID`)
);

INSERT INTO `flights` 
VALUES (311,'Korea','United States','2023-12-12 18:45:00',100,'AirlineX'),
	   (208,'Japan','Hong Kong','2023-12-15 11:30:00',150,'AirlineY'),
       (294,'Mexico','Japan','2023-12-13 22:30:00',150,'AirlineY'),
       (201,'Canada','United Kingdoms','2023-12-12 10:30:00',150,'AirlineY'),
       (231,'HKSAR','Brazil','2023-12-12 10:30:00',150,'AirlineC'),
       (200,'China','Japan','2023-12-03 10:30:00',150,'AirlineA'),
       (230,'HKSAR','Japan','2023-12-19 07:30:00',150,'AirlineD'),
       (221,'Japan','Switzerland','2023-12-01 18:30:00',150,'AirlineO'),
       (203,'Japan','Norway','2023-12-03 13:30:00',150,'AirlineQ'),
       (102,'Korea','HKSAR','2023-12-31 05:30:00',150,'AirlineA'),
       (302,'United States','Italy','2023-12-20 10:30:00',150,'AirlineY'),
       (501,'Russia','HKSAR','2023-12-31 09:30:00',150,'AirlineC'),
	   (103,'Paris','Canada','2023-11-26 21:30:00',150,'AirlineA'),
       (306,'Canada','Vancouver','2023-11-08 04:30:00',150,'AirlineY'),
       (492,'HKSAR','Dubai','2023-11-10 06:30:00',150,'AirlineD'),
	   (403,'Thailand','Dubai','2023-11-10 02:00:00',150,'AirlineQ'),
       (143,'Philippines','Dubai','2023-12-10 18:30:00',150,'AirlineO'),
	   (104,'Finland','Australia','2023-11-13 19:30:00',150,'AirlineQ'),
       (109,'Finland','New Zealand','2023-11-11 12:30:00',150,'AirlineD'),
	   (604,'Hugary','HKSAR','2023-12-03 10:30:00',150,'AirlineC');

--  Orders 

DROP TABLE IF EXISTS `orders`;
CREATE TABLE `orders` (
  `Order_ID` int NOT NULL AUTO_INCREMENT,
  `Flight_ID` int DEFAULT NULL,
  `User_ID` int DEFAULT NULL,
  `Reference_Number` VARCHAR(100) NOT NULL, 
  `Order_Date` datetime DEFAULT NULL,
  PRIMARY KEY (`Order_ID`),
  KEY `FlightID_idx` (`Flight_ID`),
  KEY `UserID_idx` (`User_ID`),
  KEY `Reference_Number_idx` (`Reference_Number`),
  CONSTRAINT `FlightID` FOREIGN KEY (`Flight_ID`) REFERENCES `flights` (`Flight_ID`),
  CONSTRAINT `UserID` FOREIGN KEY (`User_ID`) REFERENCES `users` (`User_ID`)
);


-- Refund 

DROP TABLE IF EXISTS `refunds`;
CREATE TABLE `refunds` (
  `Ticket_ID` VARCHAR(100) NOT NULL UNIQUE,
  `Reference_Number` varchar(100),
  `Remarks` LONG, 
  `Creation_Date` datetime DEFAULT NULL,
  PRIMARY KEY (`Ticket_ID`),
  KEY `Reference_Number_idx` (`Reference_Number`),
  CONSTRAINT `Reference_Number` FOREIGN KEY (`Reference_Number`) REFERENCES `orders` (`Reference_Number`)
);

-- Special Offers 
DROP TABLE IF EXISTS `special_offers`;
CREATE TABLE `special_offers` (
  `Flight_ID` int DEFAULT NULL,
  `Promotion` LONG NOT NULL, 
  KEY `FlightID_idx` (`Flight_ID`),
  CONSTRAINT `FlightID_idx` FOREIGN KEY (`Flight_ID`) REFERENCES `flights` (`Flight_ID`)
);

INSERT INTO `special_offers` 
VALUES (311,'10% Off if purchased before this coming Friday.'),
	   (208,'Enjoy 20% discount if ticket purchased using HSBC ENJOY VISA Card.');