"""The code for the movie structure that is used in the database."""

import enum

import mdb_ui as ui


class AudienceRating(enum.Enum):
    """An enum representing a rating for an audience."""

    START = enum.auto()

    G = enum.auto()
    PG = enum.auto()
    PG13 = enum.auto()
    R13 = enum.auto()
    R16 = enum.auto()
    NC18 = enum.auto()

    COUNT = enum.auto()


class Genre(enum.Enum):
    """An enum representing a genre of a movie."""

    START = enum.auto()

    ACTION = enum.auto()
    ADVENTURE = enum.auto()
    COMEDY = enum.auto()
    DRAMA = enum.auto()
    FANTASY = enum.auto()
    HORROR = enum.auto()
    MYSTERY = enum.auto()
    ROMANCE = enum.auto()
    SCIFI = enum.auto()
    THRILLER = enum.auto()
    CRIME = enum.auto()
    DOCUMENTARY = enum.auto()
    ANIMATION = enum.auto()
    FAMILY = enum.auto()
    MUSICAL = enum.auto()
    WAR = enum.auto()
    HISTORICAL = enum.auto()
    SPORT = enum.auto()

    COUNT = enum.auto()


class Movie:
    """An object that encapsulates a movie."""

    def __init__(
        self,
        id: int,
        name: str,
        release_year: int = None,
        audience_rating: str | AudienceRating = None,
        runtime: int = None,
        genre: str | list[Genre] = None,
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

        # Convert the genres and audience ratings
        if self.audience_rating is str:
            self.audience_rating = AudienceRating(self.audience_rating)

        if self.genre is str:
            self.genre = [Genre(g) for g in self.genre.split(":")]

    def get_audience_rating_value(self) -> int:
        """Convert the audience rating of this movie to an int to be stored."""
        if self.audience_rating is None:
            return None

        return self.audience_rating.value

    def get_genre_string(self) -> str | None:
        """Convert the genres of this movie to a string to be stored."""
        if self.genre is None:
            return None

        return ":".join(self.genre)

    def __str__(self):
        """Convert this movie into a string."""
        # TODO: improve this
        output = f"[{self.id}] {self.name}"

        if self.release_year is not None:
            output += f" ({self.release_year})"

        if self.audience_rating is not None:
            output += f" {self.audience_rating}"

        if self.runtime is not None:
            output += f" {self.runtime}m"

        if self.star_rating is not None:
            output += f" {ui.FULL_STAR_CHAR * self.star_rating}{ui.EMPTY_STAR_CHAR * (5 - self.star_rating)}"

        return output
