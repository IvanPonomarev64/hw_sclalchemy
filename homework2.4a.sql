INSERT INTO genre(genre_name) 
	VALUES('Jazz'), ('Rap'), ('Rnb'), ('Pop'), ('Rock');

INSERT INTO executor(executor_name) 
	VALUES('Frank Sinatra'),('Louis Armstrong'),
		('Баста'),('Eminem'),('AC/DC'),
		('Linkin Park'),('Justin Timberlake'),
		('Chris Brouwn');

INSERT INTO genre_executor(genre_id, executor_id) 
	VALUES(1,1), (1,2),
		(2,3), (2,4),
		(3,8), (4,7),
		(5,5), (5,6);

INSERT INTO album(album_name, year_of_release) 
	VALUES('My Way',1969), ('What a Wonderful World',1967),
		('Баста 40',2020), ('Music To Be Murdered By - Side B',2020),
		('Back in Black',1980), ('Living Things',2012),
		('Man of the Woods',2018), ('Indigo',2019);

INSERT INTO executor_album(executor_id, album_id) 
	values(1,1), (2,2), (3,3), (4,4),
		(5,5), (6,6), (7,7), (8,8);

INSERT INTO track(track_name, duration, album_id) 
	values('Watch What Happens', 141, 1), ('My Way', 277, 1),
		('What a Wonderful World', 140, 2), ('Hello Brother', 212, 2),
		('+100500', 348, 3), ('Любовь и страх', 320, 3),
		('Killer', 195, 4), ('No Regrets', 201, 4),
		('Back in Black', 256, 5), ('Rock and Rol Ain"t Noise Pollution', 256, 5),
		('Burn it Down', 230, 6), ('Powerless', 225, 6),
		('Supplies', 226, 7), ('Say Something', 279, 7),
		('No Guidance', 261, 8), ('Dear God', 243, 8);

INSERT INTO collection_of_songs(collection_name, year_of_release) 
	values('Сборник1', 1970), ('Сборник2', 2014),
		('Сборник3', 2018), ('Сборник4', 2019),
		('Сборник5', 2019), ('Сборник6', 2020),
		('Сборник7', 2020), ('Сборник8', 2020);

INSERT INTO track_collection(track_id, collection_of_songs_id) 
	values(1,1), (3,1), (2,2), (4,2), (9,3), (11,3), (10,4), (12,4), 
		(13,5), (15,5), (14,6), (16,6), (5,7), (7,7), (6,8), (8,8);

INSERT INTO genre_executor(genre_id, executor_id) 
	VALUES(3,7), (4,3);
	
INSERT INTO track(track_name, duration, album_id) 
	values('Белый кит', 320, 3), ('Gnat', 225, 4);