"""The code related to managing the database."""

import sqlite3

from mdb_movie import AudienceRating, Genre, Movie

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
    min_ar = AudienceRating.G.value
    max_ar = AudienceRating.NC18.value
    database.execute(f"""
    CREATE TABLE {MOVIES_TABLE} (
        ID INTEGER PRIMARY KEY,
        Name TEXT NOT NULL     CHECK(length(Name) > 0 AND length(Name) <= 100),
        ReleaseYear INTEGER    CHECK(ReleaseYear >= 1800 AND ReleaseYear <= 2100),
        AudienceRating INTEGER CHECK(AudienceRating >= {min_ar} AND AudienceRating <= {max_ar}),
        Runtime INTEGER        CHECK(Runtime > 0 AND Runtime <= 600),
        Genre TEXT,
        StarRating INTEGER     CHECK(StarRating > 0 AND StarRating <= 5),
        WhereToWatch TEXT      CHECK(length(WhereToWatch) <= 100)
    );
    """)

    # Add the initial data
    # Dummy IDs are used because they don't matter and are automatically assigned by the database
    initial_movies = [
        Movie(0, "Ghostbusters", 2016, AudienceRating.PG, 116, [Genre.COMEDY, Genre.HORROR], 4, "Netflix"),
        Movie(0, "The Legend of Tarzan", 2016, AudienceRating.PG, 109, [Genre.ACTION, Genre.ADVENTURE], 3, "Hulu"),
        Movie(0, "Jason Bourne", 2016, AudienceRating.PG, 123, [Genre.ACTION], 4, "Amazon Prime"),
        Movie(0, "The Nice Guys", 2016, AudienceRating.R13, 116, [Genre.CRIME], 4, "HBO Max"),
        Movie(0, "The Secret Life of Pets", 2016, AudienceRating.G, 91, [Genre.ANIMATION], 3, "Disney+"),
        Movie(0, "Star Trek Beyond", 2016, AudienceRating.PG, 120, [Genre.ACTION], 4, "Paramount+"),
        Movie(0, "Batman v Superman", 2016, AudienceRating.PG, 151, [Genre.ACTION], 3, "HBO Max"),
        Movie(0, "Finding Dory", 2016, AudienceRating.G, 103, [Genre.ANIMATION], 4, "Disney+"),
        Movie(0, "Zootopia", 2016, AudienceRating.G, 108, [Genre.ANIMATION], 5, "Disney+"),
        Movie(0, "The BFG", 2016, AudienceRating.PG, 90, [Genre.FANTASY], 3, "Netflix"),
        Movie(0, "A Monster Calls", 2016, AudienceRating.PG, 108, [Genre.FANTASY], 4, "Amazon Prime"),
        Movie(0, "Independence Day: Resurgence", 2016, AudienceRating.PG, 120, [Genre.ACTION], 3, "HBO Max"),
        Movie(0, "The Green Room", 2016, AudienceRating.R13, 94, [Genre.CRIME], 4, "Hulu"),
        Movie(0, "Doctor Strange", 2016, AudienceRating.PG, 130, [Genre.FANTASY], 4, "Disney+"),
        Movie(0, "The Jungle Book", 2016, AudienceRating.PG, 105, [Genre.FANTASY], 5, "Disney+"),
        Movie(0, "Alice Through the Looking Glass", 2016, AudienceRating.PG, 118, [Genre.FANTASY], 3, "Disney+"),
        Movie(0, "Imperium", 2016, AudienceRating.R13, 109, [Genre.CRIME], 4, "Hulu"),
        Movie(0, "The Infiltrator", 2016, AudienceRating.R13, 127, [Genre.CRIME], 4, "Amazon Prime"),
        Movie(0, "Mad Max: Fury Road", 2015, AudienceRating.R13, 120, [Genre.ACTION], 5, "HBO Max"),
        Movie(0, "Spectre", 2015, AudienceRating.PG, 145, [Genre.ACTION], 4, "Amazon Prime"),
        Movie(0, "Jurassic World", 2015, AudienceRating.PG, 100, [Genre.ACTION], 4, "Peacock"),
        Movie(0, "The Intern", 2015, AudienceRating.PG, 121, [Genre.COMEDY], 3, "Netflix"),
        Movie(0, "Ted 2", 2015, AudienceRating.R13, 121, [Genre.COMEDY], 3, "Amazon Prime"),
        Movie(0, "Trainwreck", 2015, AudienceRating.R13, 122, [Genre.COMEDY], 3, "HBO Max"),
        Movie(0, "Inside Out", 2015, AudienceRating.PG, 94, [Genre.ANIMATION], 5, "Disney+"),
        Movie(0, "The Good Dinosaur", 2015, AudienceRating.G, 101, [Genre.ANIMATION], 4, "Disney+"),
        Movie(0, "Divergent", 2014, AudienceRating.PG, 121, [Genre.ACTION], 3, "Netflix"),
        Movie(0, "The Maze Runner", 2014, AudienceRating.PG, 115, [Genre.ACTION], 4, "Disney+"),
        Movie(0, "Birdman", 2014, AudienceRating.R13, 119, [Genre.COMEDY], 4, "Hulu"),
        Movie(0, "Guardians of the Galaxy", 2014, AudienceRating.PG, 121, [Genre.FANTASY], 5, "Disney+"),
        Movie(0, "The Lego Movie", 2014, AudienceRating.PG, 100, [Genre.ANIMATION], 5, "Netflix"),
        Movie(0, "Big Hero 6", 2014, AudienceRating.PG, 108, [Genre.ANIMATION], 5, "Disney+"),
        Movie(0, "The Drop", 2014, AudienceRating.R13, 106, [Genre.CRIME], 4, "Hulu"),
    ]

    for movie in initial_movies:
        insert(movie)


def reset():
    """Reset the database."""
    # Delete the data and recreate the database
    database.execute(f"DROP TABLE IF EXISTS {MOVIES_TABLE};")
    database.commit()

    insert_initial_data()


def insert(movie: Movie) -> int:
    """Add an entry to the database and return the ID of the entry."""
    # According to ChatGPT, this is safer than using python string interpolation
    query = f"""
    INSERT INTO {MOVIES_TABLE} (Name, ReleaseYear, AudienceRating, Runtime, Genre, StarRating, WhereToWatch) VALUES
        (?, ?, ?, ?, ?, ?, ?);
    """

    parameters = (
        movie.name,
        movie.release_year,
        movie.audience_rating_db,
        movie.runtime,
        movie.genre_db,
        movie.star_rating,
        movie.where_to_watch,
    )

    cursor = database.cursor()
    cursor.execute(query, parameters)
    database.commit()

    return cursor.lastrowid


def edit(new_movie: Movie):
    """Edit an entry from the database by updating all of the fields using the given movie."""
    query = f"""
    UPDATE {MOVIES_TABLE} SET
        Name = ?,
        ReleaseYear = ?,
        AudienceRating = ?,
        Runtime = ?,
        Genre = ?,
        StarRating = ?,
        WhereToWatch = ?
    WHERE ID = ?;
    """

    parameters = (
        new_movie.name,
        new_movie.release_year,
        new_movie.audience_rating_db,
        new_movie.runtime,
        new_movie.genre_db,
        new_movie.star_rating,
        new_movie.where_to_watch,
        new_movie.id,
    )

    database.execute(query, parameters)
    database.commit()


def delete(id: int):
    """Delete an entry from the database via ID."""
    database.execute(f"DELETE FROM {MOVIES_TABLE} WHERE ID = ?;", (id,))
    database.commit()


def get(id: int) -> Movie:
    """Get an entry from the database via ID."""
    movie = database.execute(
        f"""
    SELECT ID, Name, ReleaseYear, AudienceRating, Runtime, Genre, StarRating, WhereToWatch
        FROM {MOVIES_TABLE} WHERE ID = ?;
    """,
        (id,),
    ).fetchone()

    if movie is None:
        return None

    return Movie(movie[0], movie[1], movie[2], AudienceRating.from_int(movie[3]), movie[4], Genre.list_from_str(movie[5]), movie[6], movie[7])


def get_all() -> list[Movie]:
    """Get all entries from the database."""
    response = database.execute(f"""
    SELECT ID, Name, ReleaseYear, AudienceRating, Runtime, Genre, StarRating, WhereToWatch
        FROM {MOVIES_TABLE};
    """)

    return [Movie(movie[0], movie[1], movie[2], AudienceRating.from_int(movie[3]), movie[4], Genre.list_from_str(movie[5]), movie[6], movie[7]) for movie in response]


def get_filter(field: str, query: str, compare_str: bool = False) -> list[Movie]:
    """Get all entries from the database with a filter."""
    response = database.execute(f"""
    SELECT ID, Name, ReleaseYear, AudienceRating, Runtime, Genre, StarRating, WhereToWatch
        FROM {MOVIES_TABLE}
        {
            f"WHERE RTRIM({field}) LIKE '%' || RTRIM(?) || '%' COLLATE NOCASE;"
            if compare_str else
            f"WHERE {field} = ?;"
        }
    """, (query,))

    return [Movie(movie[0], movie[1], movie[2], AudienceRating.from_int(movie[3]), movie[4], Genre.list_from_str(movie[5]), movie[6], movie[7]) for movie in response]
