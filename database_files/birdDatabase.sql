
CREATE TABLE Visit(
	/*
	Visits by birds during the day. Combines data from different tables
	*/

	id			INT		NOT NULL	auto_increment,
	species		VARCHAR(50),
	day			DATE,
	arrival		TIME,
	departure	TIME,
	visit_len	INT,
	accuracy	DOUBLE(3,2),

PRIMARY KEY(id),
FOREIGN KEY(species) REFERENCES Species(id)
);


CREATE TABLE Images(
	/*
	Holds all pictures of birds
	*/

	id  		INT 	NOT NULL	auto_increment,
	image  		MEDIUMBLOB,
	day			DATE,
	captureTime	TIME,
	species		VARCHAR(50),
	visit_id	INT,


PRIMARY KEY(id),
FOREIGN KEY(species) REFERENCES Species(id),
FOREIGN KEY(visit_id) REFERENCES Visit(id)
);


CREATE TABLE Species(
	/*
	Holds different names of bird species. Can only be used when recognizing species works
	*/

	id 			VARCHAR(3)		NOT NULL,
	dutchName	VARCHAR(50),
	englishName	VARCHAR(50),
	genus		VARCHAR(50),
	species		VARCHAR(50),

PRIMARY KEY(dutchName)
);


INSERT INTO Species VALUES ('KLM', 'Koolmees', 'Great Tit', 'Parus', 'major');
INSERT INTO Species VALUES ('PPM', 'Pimpelmees', 'Eurasian Blue Tit', 'Cyanistes', 'caeruleus');
INSERT INTO Species VALUES ('RDB', 'Roodborst', 'European Robin', 'Erithacus', 'rubecula');
INSERT INTO Species VALUES ('HSM', 'Huismus', 'House Sparrow', 'Passer', 'domesticus');
INSERT INTO Species VALUES ();
INSERT INTO Species VALUES ();
INSERT INTO Species VALUES ();