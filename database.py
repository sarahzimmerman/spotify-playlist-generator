"""Defines all the functions related to the database"""
from app import db
from datetime import datetime
import random
import string

def fetch_albums():
    """Reads all albums listed in the album table

    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    query_results = conn.execute("SELECT title, numSongs, totalDuration FROM Playlist LIMIT 10;").fetchall()
    conn.close()
    album_list = []
    for result in query_results:
        album = {
            "title": result[0],
            "numSongs":result[1],
            "totalDuration":result[2]
        }
        album_list.append(album)
    return album_list

def fetch_songs_advanced(genre: str, start_date: int, end_date: int):
    """Reads all tasks listed in the todo table

    Returns:
        A list of dictionaries
    """
    conn = db.connect()
    genre = "%" + genre + "%"
    start_date = str(start_date)+"-01-01"
    end_date = str(end_date)+"-12-31"
    # print(start_date)
    query = 'SELECT name, a.popularity FROM (SELECT name, albumID FROM Song WHERE genre LIKE %s AND releaseDate >= "{}" AND releaseDate < "{}" ) AS s INNER JOIN (SELECT albumID, popularity FROM Album WHERE popularity > 5) AS a ON (s.albumID=a.albumID) ORDER BY a.popularity DESC LIMIT 15;'.format(start_date, end_date)
    # print(query)
    query_results = conn.execute(query, genre).fetchall()
    conn.close()
    song_list = []
    for result in query_results:
        song = {
            "name": result[0],
            "popularity": result[1]
        }
        song_list.append(song)
    return song_list

def above_avg_playtime():
    """Reads all tasks listed in the todo table

    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    query = '''SELECT p.playlistID, p.numSongs, p.totalDuration, p.Title
                FROM Playlist p
                WHERE p.totalDuration > (SELECT AVG(p1.totalDuration) 
                FROM Playlist p1 GROUP BY p1.minYear, p1.maxYear 
                HAVING p1.minYear = p.minYear AND p1.maxYear = p.maxYear) 
                ORDER BY p.totalDuration DESC;'''
    query_results = conn.execute(query).fetchall()
    conn.close()
    above_avg_play_list = []
    for result in query_results:
        item = {
            "playlistID": result[0],
            "numSongs": result[1],
            "totalDuration": result[2],
            "title":result[3]
        }
        above_avg_play_list.append(item)

    return above_avg_play_list


def update_song(song_id: int, name: str, genre: str) -> None:
    conn = db.connect()
    if name == "":
        query = 'UPDATE Song SET genre = "{}" WHERE id = {};'.format(genre, song_id)
    elif genre == "":
        query = 'UPDATE Song SET name = "{}" WHERE id = {};'.format(name, song_id)
    else:
        query = 'UPDATE Song SET name = "{}" AND genre = "{}" WHERE id = {};'.format(name, genre, song_id)
    conn.execute(query)
    conn.close()
    
def update_artist(artist_id: string, popularityRating: int) -> None:
    conn = db.connect()
    print(artist_id, " DB ", popularityRating, " pop ")
    query = 'UPDATE Artist SET popularityRating = {} WHERE artistID = "{}";'.format(popularityRating, artist_id)
    conn.execute(query)
    conn.close()


def insert_new_artist(name: str, followers: int, image: str, popularityRating: int) ->  int:
    """Insert new artist to Artist table.

    Args:
        text (str): Task description

    Returns: The artist ID for the inserted entry
    """

    conn = db.connect()
    pk = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for x in range(22))
    query = 'INSERT INTO Artist VALUES ("{}", "{}", "{}", "{}", "{}");'.format(
        pk, name, followers, image, popularityRating)
    print(pk, name, followers, image, popularityRating)
    conn.execute(query)
    query_results = conn.execute("SELECT LAST_INSERT_ID();")
    query_results = [x for x in query_results]
    artist_id = query_results[0][0]
    conn.close()

    return artist_id


def remove_artist_by_id(artist_id: str) -> None:
    """ remove entries based on task ID """
    print(artist_id, " DB DELETE ")
    conn = db.connect()
    query = 'DELETE FROM Artist WHERE artistID="{}";'.format(artist_id)
    conn.execute(query)
    conn.close()

def fetch_artist_name(artistName: str): 
    conn = db.connect()
    artistName = "%" + artistName + "%"
    query = 'SELECT artistID, name, followers, image, popularityRating FROM Artist WHERE name LIKE %s ORDER BY popularityRating DESC LIMIT 25;'
    print(query)
    query_results = conn.execute(query, artistName).fetchall()
    print(query_results)
    conn.close()
    artist_list = []
    for result in query_results:
        artist = {
            "artistID": result[0],
            "name":result[1],
            "followers": result[2],
            'image': result[3],
            'popularityRating': result[4]
        }
        artist_list.append(artist)

    return artist_list


def fetch_artist():
    """Reads all artists listed in the artists table

    Returns:
        A list of dictionaries
    """
    conn = db.connect()
    query_results = conn.execute("SELECT artistID, name, followers, image, popularityRating FROM Artist ORDER BY popularityRating DESC LIMIT 20 ;").fetchall()
    conn.close()
    artist_list = []
    for result in query_results:
        artist = {
            "artistID": result[0],
            "name":result[1],
            "followers": result[2],
            'image': result[3],
            'popularityRating': result[4]
        }
        artist_list.append(artist)

    return artist_list

def song_trigger():
    conn = db.connect()
    trigger = "CREATE TRIGGER SongsTrig BEFORE INSERT ON Song FOR EACH ROW BEGIN IF (NEW.releaseDate IS NULL) THEN UPDATE Album SET releaseDate = %s WHERE albumID = NEW.albumID; SET NEW.releaseDate = %s;  END IF; END;"
    try: 
        date = "2022-01-01"
        conn.execute(trigger, (date, date))
        conn.close()
        print("Trigger on Song created")
    except:
        print("Exception occured")

def era_stored_procedure():
    conn = db.connect()
    with open('stored_procedure.sql', 'r') as f:
        stored_procedure = f.read()
    print("stored procedure: ", stored_procedure)
    try:
        conn.execute(stored_procedure)
        conn.close()
        print("Stored procedure executed")
    except:
        print("Exception occured on stored procedure")

def insert_new_song(name: str, genre: str, popularity: int, totalDuration: float, albumID: str):
    print("hello")
    conn = db.connect()
    pk = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for x in range(22))
    print("Inserting into Song : ", pk, name, genre, popularity, totalDuration)
    query = 'INSERT INTO Song(songID, name, genre, popularity, totalDuration, releaseDate, albumID) VALUES ("{}", "{}", "{}", "{}", "{}", %s, "{}");'.format(
        pk, name, genre, popularity, totalDuration)
    try:
        conn.execute(query, None)
        print("Inserted into Song : ", pk, name, genre, popularity, totalDuration)
    except:
        print("failed to insert")
    query_results = conn.execute("SELECT LAST_INSERT_ID();")
    query_results = [x for x in query_results]
    song_id = query_results[0][0]
    conn.close()

    return song_id