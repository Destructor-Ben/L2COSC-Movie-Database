"""The code related to managing the database."""

import sqlite3

MOVIES_TABLE = "MOVIES"

database: sqlite3.Connection = None


def setup():
    """Set up the database utilities.

    Must be called before anything else in this file to guarantee proper functionality.
    """
    global database

    # Connect to the database and add the initial data if it doesn't exist
    database = sqlite3.connect("Database.db")
    insert_initial_data()


def insert_initial_data():
    """Add the initial contents of the database if it doesn't exist."""
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
    # TODO: more initial data
    database.execute(f"""
    INSERT INTO {MOVIES_TABLE} (Name) VALUES
        ('Batman'),
        ('Joker'),
        ('Iron Man'),
        ('Spiderman: Into the Spiderverse');
    """)

    database.execute(f"""
    INSERT INTO {MOVIES_TABLE} (Name, ReleaseYear, AudienceRating, Runtime, Genre, StarRating, WhereToWatch) VALUES
        ('FizzBuzz', 2001, 'R-16', 102, 'Romance', 9, 'https://example.com');
    """)

    database.commit()


def reset():
    """Reset the database."""
    # Delete the data and recreate the database
    database.execute(f"DROP TABLE IF EXISTS {MOVIES_TABLE};")
    insert_initial_data()


def debug_print():
    """Print the contents of the database to the console."""
    print(f"{MOVIES_TABLE}:")
    for row in database.execute(f"SELECT * FROM {MOVIES_TABLE}"):
        print("  " + str(row))
