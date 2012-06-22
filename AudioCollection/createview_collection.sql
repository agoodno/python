CREATE OR REPLACE VIEW collection AS
	SELECT ar.name AS artistName, al.name AS albumName, t.num AS trackNum, t.name AS trackName
	FROM artist ar
	JOIN album al ON (al.artist_id = ar.id)
	JOIN track t ON (t.album_id = al.id)
	ORDER BY artistName, al.year, t.num;
