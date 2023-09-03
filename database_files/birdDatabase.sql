DROP TABLE IF EXISTS Image;
DROP TABLE IF EXISTS Visit;
DROP TABLE IF EXISTS Species;

CREATE TABLE Species(
-- Holds different names of bird species. Can only be used when recognizing species works

	id VARCHAR(3) NOT NULL UNIQUE,
	dutchName VARCHAR(50),
	englishName VARCHAR(50),
	genus VARCHAR(50),
	species VARCHAR(50),

	PRIMARY KEY(id)
);

CREATE TABLE Visit(
-- Visits by birds during the day. Combines data from different tables

	visit_id VARCHAR(64),
	species VARCHAR(50),
	arrival DATETIME NOT NULL,
	departure DATETIME DEFAULT NULL,
	visit_len INT NOT NULL,
	accuracy DECIMAL(5, 2),

	PRIMARY KEY(visit_id),
	FOREIGN KEY(species) REFERENCES Species(id)
);


CREATE TABLE Image(
-- Holds all images of birds

	rec_id INT 	NOT NULL AUTO_INCREMENT,
	image_id VARCHAR(64) NOT NULL,
	image_name TINYTEXT NOT NULL,
	classification ENUM('Bird', 'False', 'undef') NOT NULL,
	accuracy_class DECIMAL(5, 2) NOT NULL,
	visit_id VARCHAR(64),
	species VARCHAR(50),
	accuracy_species DECIMAL(5, 2),
	timestamp DATETIME NOT NULL,
	date DATE NOT NULL,
	time TIME NOT NULL,


	PRIMARY KEY(rec_id),
	FOREIGN KEY(species) REFERENCES Species(id),
	FOREIGN KEY(visit_id) REFERENCES Visit(visit_id)
);



