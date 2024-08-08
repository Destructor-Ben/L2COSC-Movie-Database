"""The code related to managing the database."""

import sqlite3

MOVIES_TABLE = "MOVIES"

database: sqlite3.Connection = None

# TODO: finish this file


def setup():
    """Set up the database utilities.

    Must be called before anything else in this file to guarantee proper functionality.
    """
    global database

    database = sqlite3.connect("Database.db")

    # Delete existing data
    database.execute(f"DROP TABLE IF EXISTS {MOVIES_TABLE}")

    # Create the table
    database.execute(f"""
    CREATE TABLE {MOVIES_TABLE} (
        ID INT PRIMARY KEY,
        Name TINYTEXT
    )
    """)

    # Add the initial data
    database.execute(f"INSERT INTO {MOVIES_TABLE} VALUES (0, 'TEST')")

    # Save
    database.commit()


def debug_print():
    """Print the contents of the database to the console."""
    print(f"{MOVIES_TABLE}:")
    for row in database.execute(f"SELECT * FROM {MOVIES_TABLE}"):
        print("  " + str(row))
