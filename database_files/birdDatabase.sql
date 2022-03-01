
CREATE DATABASE IF NOT EXISTS birdDatabase;
USE birdDatabase;

DROP TABLE IF EXISTS Visit;
DROP TABLE IF EXISTS Images;
DROP TABLE IF EXISTS Species;



CREATE TABLE Species(
	/*
	Holds different names of bird species. Can only be used when recognizing species works
	*/

	id VARCHAR(3) NOT NULL UNIQUE,
	dutchName VARCHAR(50),
	englishName VARCHAR(50),
	genus VARCHAR(50),
	species VARCHAR(50),

	PRIMARY KEY(id)
);

CREATE TABLE Visit(
	/*
	Visits by birds during the day. Combines data from different tables
	*/

	id INT NOT NULL,
	species VARCHAR(50),
	day DATE,
	arrival TIME,
	departure TIME,
	visit_len INT,
	accuracy DOUBLE(3,2),

	PRIMARY KEY(id),
	FOREIGN KEY(species) REFERENCES Species(id)
);


CREATE TABLE Images(
	/*
	Holds all pictures of birds
	*/

	id INT 	NOT NULL AUTO_INCREMENT,
	image_name TINYTEXT,
	capture_day DATETIME,
	species VARCHAR(50),
	visit_id INT,


	PRIMARY KEY(id),
	FOREIGN KEY(species) REFERENCES Species(id),
	FOREIGN KEY(visit_id) REFERENCES Visit(id)
);



