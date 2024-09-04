"""The code for the movie structure that is used in the database."""

import enum


# TODO: actually use this enum
class AudienceRating(enum.Enum):
    """An enum representing a rating for an audience."""
    G = enum.auto()
    PG = enum.auto()
    PG13 = enum.auto()
    R13 = enum.auto()
    R16 = enum.auto()
    NC18 = enum.auto()


# TODO: constraints & datatype conversions
class Movie:
    """An object that encapsulates a movie."""

    def __init__(
        self,
        id: int,
        name: str,
        release_year: int = None,
        audience_rating: str = None,
        runtime: int = None,
        genre: str = None,
        star_rating: int = None,
        where_to_watch: str = None,
    ):
        """Create a movie with the given parameters."""
        self.id = id
        self.name = name
        self.release_year = release_year
        self.audience_rating = audience_rating
        self.runtime = runtime
        self.genre = genre
        self.star_rating = star_rating
        self.where_to_watch = where_to_watch

    # TODO: temporary
    def __str__(self):
        return f"[{self.id}] {self.name} <{self.audience_rating}> <{self.release_year}> <{self.runtime}m> <{self.genre}> <{self.star_rating}> <{self.where_to_watch}>"
