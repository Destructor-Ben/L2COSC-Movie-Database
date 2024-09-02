"""The code related to managing the database."""

import sqlite3

from mdb_movie import Movie

MOVIES_TABLE = "MOVIES"

database: sqlite3.Connection = None


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
        SELECT (ID, Name, ReleaseYear, AudienceRating, Runtime, Genre, StarRating, WhereToWatch)
            FROM {MOVIES_TABLE} WHERE ID = {id};
    """)

    return Movie(response[0], response[1], response[2], response[3], response[4], response[5], response[6], response[7])


def get_all() -> list[Movie]:
    """Get all entries from the database."""
    response = database.execute(f"""
    SELECT (ID, Name, ReleaseYear, AudienceRating, Runtime, Genre, StarRating, WhereToWatch)
        FROM {MOVIES_TABLE};
    """)

    return [Movie(movie[0], movie[1], movie[2], movie[3], movie[4], movie[5], movie[6], movie[7]) for movie in response]
