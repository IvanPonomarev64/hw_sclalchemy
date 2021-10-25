SELECT g.genre_name, count(ge.executor_id) FROM genre g
   JOIN genre_executor ge ON g.id = ge.genre_id
   GROUP BY g.genre_name;
   
SELECT a.album_name, a.year_of_release, count(t.id) FROM album a
   JOIN track t ON a.id = t.album_id
   WHERE a.year_of_release BETWEEN 2019 and 2020
   GROUP BY a.album_name, a.year_of_release;
  
SELECT a.album_name, AVG(t.duration) FROM album a
	JOIN track t ON a.id = t.album_id
	GROUP BY a.album_name;

SELECT e.executor_name FROM executor e
   JOIN executor_album ea ON e.id = ea.executor_id
   JOIN album a ON a.id = ea.album_id
   WHERE a.year_of_release < 2020; 
  
SELECT c.collection_name FROM collection_of_songs c
   JOIN track_collection tc ON c.id = tc.collection_of_songs_id
   JOIN track t ON t.id = tc.track_id
   JOIN album a ON a.id = t.album_id
   JOIN executor_album ea ON a.id = ea.album_id
   JOIN executor e ON e.id = ea.executor_id
   WHERE e.executor_name LIKE '%%Баста%%';
  
SELECT a.album_name FROM album a
	JOIN executor_album ea ON a.id = ea.album_id
	JOIN executor e ON e.id = ea.executor_id
	JOIN genre_executor ge ON ge.executor_id = e.id
	JOIN genre g ON g.id = ge.genre_id
	GROUP BY e.executor_name, a.album_name
    HAVING count(ge.genre_id) > 1;
   
SELECT t.track_name FROM track t
	LEFT JOIN  track_collection tc ON t.id = tc.track_id
	WHERE tc.track_id IS null;
	
SELECT e.executor_name FROM executor e
	JOIN executor_album ea ON e.id = ea.executor_id
	JOIN album a ON a.id = ea.album_id
	JOIN track t ON t.album_id = a.id
	WHERE duration = (SELECT MIN(duration) FROM track);

SELECT a.album_name , count(t.id) FROM album a
    JOIN track t ON a.id = t.album_id
    GROUP BY a.album_name 
    HAVING count(t.id) in (
    	SELECT count(t.id) FROM album a
    	JOIN track t ON a.id = t.album_id
        GROUP BY a.album_name
        ORDER BY count(t.id)
        LIMIT 1);
	