"""The code related to managing the database."""

import sqlite3

from mdb_movie import Movie

MOVIES_TABLE = "MOVIES"

database: sqlite3.Connection = None

"""Movies to be added:
001,Ghostbusters,2016,PG,116,Comedy
002,The Legend of Tarzan,2016,PG,109,Action
003,Jason Bourne,2016,PG,123,Action
004,The Nice Guys,2016,R,116,Crime
005,The Secret Life of Pets,2016,G,91,Animation
006,Star Trek Beyond,2016,PG,120,Action
007,Batman v Superman,2016,PG,151,Action
008,Finding Dory,2016,G,103,Animation
009,Zootopia,2016,G,108,Animation
010,The BFG,2016,PG,90,Fantasy
011,A Monster Calls,2016,PG,108,Fantasy
012,Independence Day: Resurgence,2016,PG,120,Action
013,The Green Room,2016,R,94,Crime
014,Doctor Strange,2016,PG,130,Fantasy
015,The Jungle Book,2016,PG,105,Fantasy
016,Alice Through the Looking Glass,2016,PG,118,Fantasy
017,Imperium,2016,R,109,Crime
018,The Infiltrator,2016,R,127,Crime
019,Mad Max: Fury Road,2015,R,120,Action
020,Spectre,2015,PG,145,Action
021,Jurassic World,2015,PG,100,Action
022,The Intern,2015,PG,121,Comedy
023,Ted 2,2015,R,121,Comedy
024,Trainwreck,2015,R,122,Comedy
025,Inside Out,2015,PG,94,Animation
026,The Good Dinosaur,2015,G,101,Animation
027,Divergent,2014,PG,121,Action
028,The Max Runner,2014,PG,115,Action
029,Birdman,2014,R,119,Comedy
030,Guardians of the Galaxy,2014,PG,121,Fantasy
031,The Lego Movie,2014,PG,100,Animation
032,Big Hero 6,2014,PG,108,Animation
033,The Drop,2014,R,106,Crime
"""


def setup():
    """Set up the database utilities.

    Must be called before anything else in this file to guarantee proper functionality.
    """
    global database

    # Connect to the database and add the initial data if it doesn"t exist
    database = sqlite3.connect("Database.db")
    insert_initial_data()


def insert_initial_data():
    """Add the initial contents of the database if it doesn"t exist."""
    # Check if the table exists already
    response = database.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{MOVIES_TABLE}';")
    if len(response.fetchall()) > 0:
        return

    # Create the table
    # TODO: contraints
    database.execute(f"""
    CREATE TABLE {MOVIES_TABLE} (
        ID INTEGER PRIMARY KEY,
        Name TEXT NOT NULL,
        ReleaseYear INTEGER,
        AudienceRating TEXT,
        Runtime INTEGER,
        Genre TEXT,
        StarRating INTEGER,
        WhereToWatch TEXT
    );
    """)

    # Add the initial data
    # Dummy IDs are used because they don't matter and are automatically assigned by the database
    # TODO: more initial data
    insert(Movie(0, "FizzBuzz", 2001, "R-16", 102, "Romance", 1, "https://example.com"))
    insert(Movie(0, "Among Us", 2020, "NC-18", 69420, "Horror", 5, "https://sigma.com"))
    insert(Movie(0, "FNAF", 1987, "PG-13", 167, "Thriller", 4, "https://fnaf.com"))

    for i in range(15):
        insert(Movie(0, "a" * i))


def reset():
    """Reset the database."""
    # Delete the data and recreate the database
    database.execute(f"DROP TABLE IF EXISTS {MOVIES_TABLE};")
    database.commit()

    insert_initial_data()


def insert(movie: Movie):
    """Add an entry to the database."""
    # According to ChatGPT, this is safer than using python string interpolation
    query = f"""
    INSERT INTO {MOVIES_TABLE} (Name, ReleaseYear, AudienceRating, Runtime, Genre, StarRating, WhereToWatch) VALUES
        (?, ?, ?, ?, ?, ?, ?);
    """

    parameters = (
        movie.name,
        movie.release_year,
        movie.audience_rating,
        movie.runtime,
        movie.genre,
        movie.star_rating,
        movie.where_to_watch,
    )

    database.execute(query, parameters)
    database.commit()


def edit(new_movie: Movie):
    """Edit an entry from the database by updating all of the fields using the given movie."""
    query = f"""
    UPDATE {MOVIES_TABLE} SET (
        Name = ?,
        ReleaseYear = ?,
        AudienceRating = ?,
        Runtime = ?,
        Genre = ?,
        StarRating = ?,
        WhereToWatch = ?
    ) WHERE ID = {new_movie.id};
    """

    parameters = (
        new_movie.name,
        new_movie.release_year,
        new_movie.audience_rating,
        new_movie.runtime,
        new_movie.genre,
        new_movie.star_rating,
        new_movie.where_to_watch,
    )

    database.execute(query, parameters)
    database.commit()


def delete(id: int):
    """Delete an entry from the database via ID."""
    database.execute(f"DELETE FROM {MOVIES_TABLE} WHERE ID = {id};")


def get(id: int) -> Movie:
    """Get an entry from the database via ID."""
    response = database.execute(f"""
    SELECT ID, Name, ReleaseYear, AudienceRating, Runtime, Genre, StarRating, WhereToWatch
        FROM {MOVIES_TABLE} WHERE ID = {id};
    """)

    return Movie(response[0], response[1], response[2], response[3], response[4], response[5], response[6], response[7])


def get_all() -> list[Movie]:
    """Get all entries from the database."""
    response = database.execute(f"""
    SELECT ID, Name, ReleaseYear, AudienceRating, Runtime, Genre, StarRating, WhereToWatch
        FROM {MOVIES_TABLE};
    """)

    return [Movie(movie[0], movie[1], movie[2], movie[3], movie[4], movie[5], movie[6], movie[7]) for movie in response]
