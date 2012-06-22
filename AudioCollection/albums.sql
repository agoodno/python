SELECT art.name AS artistName, alb.name AS albumName, trk.name AS trackName
FROM Track trk
JOIN Album alb ON (alb.id = trk.album_id)
JOIN Artist art ON (art.id = alb.artist_id);

