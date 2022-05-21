USE Rewind;
DELIMITER //        
CREATE PROCEDURE eras()
 BEGIN
    DECLARE varSongID VARCHAR(50);
    DECLARE varSongName VARCHAR(255);
    DECLARE varAlbumName VARCHAR(255);
    DECLARE varReleaseDate VARCHAR(50);
    DECLARE Era VARCHAR(50);
    DECLARE loop_exit BOOLEAN DEFAULT FALSE;

    DECLARE cur CURSOR FOR (SELECT s.songID, s.songName, a.albumName, a.releaseDate
                            FROM (
                                    SELECT songID, name AS songName, albumID FROM Song WHERE popularity > 5
                                ) as s 
                                NATURAL JOIN (
                                    SELECT name AS albumName, releaseDate, albumID FROM Album WHERE releaseDate >= "1880-01-01"
                                ) as a ORDER BY popularity LIMIT 50 
                            );

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET loop_exit = TRUE;

    DROP TABLE IF EXISTS SongEra;
    CREATE TABLE SongEra (
        songID VARCHAR(50) PRIMARY KEY,
        songName VARCHAR(255),
        albumName VARCHAR(255),
        era VARCHAR(50)
    );

    OPEN cur;
    cloop: LOOP
        FETCH cur INTO varSongID, varSongName, varAlbumName, varReleaseDate;
        IF (loop_exit) THEN
            LEAVE cloop;
        END IF;

        IF (varReleaseDate < 1920) THEN 
            SET Era = 'Antique';
        ELSEIF (varReleaseDate < 1960) THEN
            SET Era = 'Vintage';
        ELSEIF (varReleaseDate < 2000) THEN
            SET Era = 'Classic';
        ELSEIF (varReleaseDate >= 2000) THEN
            SET Era = 'Contemporary';
        END IF;

        INSERT IGNORE INTO SongEra VALUES(varSongID, varSongName, varAlbumName, Era);
    END LOOP cloop;
    CLOSE cur;    
    
    SELECT * FROM SongEra JOIN (SELECT SongID, genre FROM Song) as songInfo USING (SongID);
END //

DELIMITER ;    
