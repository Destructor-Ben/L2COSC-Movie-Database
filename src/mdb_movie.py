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

    def __str__(self):
        """Convert this object to a string."""
        match self:
            case AudienceRating.G:
                return "G"
            case AudienceRating.PG:
                return "PG"
            case AudienceRating.PG13:
                return "PG-13"
            case AudienceRating.R13:
                return "R-13"
            case AudienceRating.R16:
                return "R-16"
            case AudienceRating.NC18:
                return "NC-18"


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

    def __str__(self):
        """Convert this object to a string."""
        name = self.name.lower()
        return name[0].upper() + name[1:]


# TODO: possible make the way the input and output of this class handled better
# Could do this with properties
# Also make where_to_watch an enum
class Movie:
    """An object that encapsulates a movie."""

    def __init__(
        self,
        id: int,
        name: str,
        release_year: int = None,
        audience_rating: int | AudienceRating = None,
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
        if type(self.audience_rating) is int:
            self.audience_rating: AudienceRating = AudienceRating(self.audience_rating)

        if type(self.genre) is str:
            self.genre: list[Genre] = [Genre(int(g)) for g in self.genre.split(":")]

    def get_audience_rating_value(self) -> int:
        """Convert the audience rating of this movie to an int to be stored."""
        if self.audience_rating is None:
            return None

        return self.audience_rating.value

    def get_genre_string(self) -> str | None:
        """Convert the genres of this movie to a string to be stored."""
        if self.genre is None:
            return None

        return ":".join(map(lambda g: str(g.value), self.genre))

    def __str__(self):
        """Convert this movie into a string."""
        output = f"[{self.id}] {self.name}"

        if self.release_year is not None:
            output += f" ({self.release_year})"

        if self.audience_rating is not None:
            output += f" {self.audience_rating}"

        if self.star_rating is not None:
            output += f" {ui.FULL_STAR_CHAR * self.star_rating}{ui.EMPTY_STAR_CHAR * (5 - self.star_rating)}"

        return output
