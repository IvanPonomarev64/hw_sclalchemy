SELECT album_name, year_of_release FROM album    
	WHERE year_of_release = 2018;

SELECT track_name, duration FROM track    
	ORDER BY duration DESC
	LIMIT 1;
	
SELECT track_name FROM track 
	WHERE duration >= 210;
	
SELECT collection_name FROM collection_of_songs 
	WHERE year_of_release BETWEEN 2018 and 2020;
	
SELECT executor_name FROM executor
	WHERE executor_name NOT LIKE '%% %%';
	
SELECT track_name FROM track
	WHERE track_name LIKE '%%My%%';