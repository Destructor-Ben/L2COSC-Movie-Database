"""The code for the movie structure that is used in the database."""

import enum

import mdb_ui as ui


# TODO: make in insert and edit menus make it clearer what these stand for, e.g. PG -> Parental Guidance
class AudienceRating(enum.Enum):
    """An enum representing a rating for an audience."""

    G = enum.auto()
    PG = enum.auto()
    PG13 = enum.auto()
    R13 = enum.auto()
    R16 = enum.auto()
    NC18 = enum.auto()

    @staticmethod
    def from_str(value: str):
        """Get an audience rating from a string."""
        # Empty string
        if value is None or value.strip() == "":
            return None

        # If its an int, then parse from int
        try:
            number = int(value)
            return AudienceRating.from_int(number)
        except:
            pass

        # Otherwise, assume its the name of the enum
        key = value.strip().upper().replace("-", "")
        if key in AudienceRating._member_map_:
            return AudienceRating._member_map_[key]

        # Not a valid enum member
        return None

    @staticmethod
    def from_int(value: int):
        """Get an audience rating from an int."""
        if value is None or value < AudienceRating.G.value or value > AudienceRating.NC18.value:
            return None

        return AudienceRating(value)

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

    @staticmethod
    def list_from_str(value: str):
        """Get a list of genres from a string."""
        # Empty string
        if value is None or value.strip() == "":
            return None

        return list(map(lambda g: Genre.from_str(g), value.split(":")))

    @staticmethod
    def from_str(value: str):
        """Get a genre from a string."""
        # Empty string
        if value is None or value.strip() == "":
            return None

        # If its an int, then parse from int
        try:
            number = int(value)
            return Genre.from_int(number)
        except:
            pass

        # Otherwise, assume its the name of the enum
        key = value.strip().upper()
        if key in Genre._member_map_:
            return Genre._member_map_[key]

        # Not a valid enum member
        return None

    @staticmethod
    def from_int(value: int):
        """Get a genre from an int."""
        if value is None or value < Genre.ACTION.value or value > Genre.SPORT.value:
            return None

        return Genre(value)

    def __str__(self):
        """Convert this object to a string."""
        name = self.name.lower()
        return name[0].upper() + name[1:]


class MovieField(enum.Enum):
    """An enum representing an ID for a field from a movie."""

    ID = enum.auto()
    NAME = enum.auto()
    RELEASE_YEAR = enum.auto()
    AUDIENCE_RATING = enum.auto()
    RUNTIME = enum.auto()
    GENRE = enum.auto()
    STAR_RATING = enum.auto()
    WHERE_TO_WATCH = enum.auto()

    @property
    def database_name(self) -> str:
        """Get the name of this field in the database."""
        match self:
            case MovieField.ID:
                return "ID"
            case MovieField.NAME:
                return "Name"
            case MovieField.RELEASE_YEAR:
                return "ReleaseYear"
            case MovieField.AUDIENCE_RATING:
                return "AudienceRating"
            case MovieField.RUNTIME:
                return "Runtime"
            case MovieField.GENRE:
                return "Genre"
            case MovieField.STAR_RATING:
                return "StarRating"
            case MovieField.WHERE_TO_WATCH:
                return "WhereToWatch"
            case _:
                return "???"

    @staticmethod
    def from_str(value: str):
        """Get a movie field from a string."""
        # Empty string
        if value is None or value.strip() == "":
            return None

        # If its an int, then parse from int
        try:
            number = int(value)
            return MovieField.from_int(number)
        except:
            pass

        # Otherwise, assume its the name of the enum
        key = value.strip().upper()
        if key in MovieField._member_map_:
            return MovieField._member_map_[key]

        # Not a valid enum member
        return None

    @staticmethod
    def from_int(value: int):
        """Get a movie field from an int."""
        if value is None or value < MovieField.ID.value or value > MovieField.WHERE_TO_WATCH.value:
            return None

        return MovieField(value)

    def validate_field(self, user_input: str, enforce_name: bool = False) -> tuple[bool, any, str | None]:
        """Check if the given user input is valid for this movie field.
        
        Returns a tuple: (Valid (None if the field isn't required), ParsedValue, ErrorMessage | None)
        """
        # Convert empty input into None if it's empty
        user_input = user_input.strip()
        if user_input == "":
            user_input = None

        match self:
            case MovieField.NAME:
                if user_input is None:
                    if enforce_name:
                        return (False, user_input, "No movie name was given")
                    else:
                        return (None, None, None)

                if len(user_input) > 100:
                    return (False, user_input, "The entered movie name is longer than 100 characters")
                
                return (True, user_input, None)
            case MovieField.RELEASE_YEAR:
                # Make this optional
                if user_input is None:
                    return (None, None, None)

                try:
                    value = int(user_input)
                    if value < 1800:
                        return (False, value, "The release year entered is smaller than 1800")

                    if value > 2100:
                        return (False, value, "The release year entered is greater than 2100")

                    return (True, value, None)
                except:
                    return (False, user_input, "The release year entered isn't an integer")
            case MovieField.AUDIENCE_RATING:
                # Make this optional
                if user_input is None:
                    return (None, None, None)

                value = AudienceRating.from_str(user_input)
                if value is None:
                    return (False, user_input, "The audience rating entered isn't valid")

                return (True, value, None)
            case MovieField.RUNTIME:
                # Make this optional
                if user_input is None:
                    return (None, None, None)

                try:
                    value = int(user_input)
                    if value < 1:
                        return (False, value, "The runtime entered is smaller than 1")

                    if value > 600:
                        return (False, value, "The runtime entered is greater than 600")

                    return (True, value, None)
                except:
                    return (False, user_input, "The runtime entered isn't an integer")
            case MovieField.GENRE:
                # Make this optional
                if user_input is None:
                    return (None, None, None)

                # Parse
                value = list(map(lambda g: Genre.from_str(g.strip()), user_input.split(",")))

                # Check if there are any invalid genres in the list
                if None in value:
                    # TODO: this is an unclear error message
                    return (False, value, "One of the entered genres is invalid")

                return (True, value, None)
            case MovieField.STAR_RATING:
                # Make this optional
                if user_input is None:
                    return (None, None, None)

                try:
                    value = int(user_input)
                    if value < 0:
                        return (False, value, "The star rating entered is smaller than 0")

                    if value > 5:
                        return (False, value, "The star rating entered is greater than 5")

                    return (True, value, None)
                except:
                    return (False, user_input, "The star rating entered isn't an integer")
            case MovieField.WHERE_TO_WATCH:
                # Make this optional
                if user_input is None:
                    return (None, None, None)

                if len(user_input) > 100:
                    return (False, user_input, "The entered watch location is longer than 100 characters")

                return (True, user_input, None)
            # Error case (never will happen because im smart)
            case _:
                return (False, user_input, f"Unknown movie field: {self}")

    # TODO: reduce duplication
    def get_insert_prompt(self) -> str:
        """Get a prompt for this field for when the user is entering the value for this field."""
        message = f"Invalid movie field: {self}"

        match self:
            case MovieField.NAME:
                message = "What is the name of the movie?"
                message += "\nRequired"
                message += "\nMax 100 characters"
            case MovieField.RELEASE_YEAR:
                message = "What is the release year of the movie?"
                message += "\nPress Enter to skip"
                message += "\nMust be between 1800 and 2100 (inclusive)"
            case MovieField.AUDIENCE_RATING:
                message = "What is the audience rating of the movie?"
                message += "\nPress Enter to skip"
                message += "\nValid Audience Ratings:"
                for rating in AudienceRating:
                    message += f"\n- {rating}"
            case MovieField.RUNTIME:
                message = "What is the runtime of the movie in minutes?"
                message += "\nPress Enter to skip"
                message += "\nMust be between 1 and 600 (inclusive)"
            case MovieField.GENRE:
                message = "What are the genres of the movie? (enter a comma separated list)"
                message += "\nPress Enter to skip"
                message += "\nAvailable genres:"

                # Create the genre list by breaking it into 3 lines
                genres = list(Genre)
                num_lines = 3
                for i in range(num_lines):
                    chunk_size = len(genres) // num_lines
                    start_index = i * chunk_size
                    end_index = i * chunk_size + chunk_size

                    line_genres = genres[start_index:end_index]
                    message += "\n"
                    message += ", ".join(map(lambda g: str(g), line_genres))
            case MovieField.STAR_RATING:
                message = "What is the star rating of the movie?"
                message += "\nPress Enter to skip"
                message += "\nMust be between 0 and 5 (inclusive)"
            case MovieField.WHERE_TO_WATCH:
                message = "Where can the movie be watched?"
                message += "\nPress Enter to skip"
                message += "\nMax 100 characters"

        return message

    def get_edit_prompt(self) -> str:
        """Get a prompt for this field for when the user is editing value for this field."""
        message = f"Invalid movie field: {self}"

        match self:
            case MovieField.NAME:
                message = "What is the new name of the movie?"
                message += "\nPress Enter to skip"
                message += "\nMax 100 characters"
            case MovieField.RELEASE_YEAR:
                message = "What is the new release year of the movie?"
                message += "\nPress Enter to skip"
                message += "\nMust be between 1800 and 2100 (inclusive)"
            case MovieField.AUDIENCE_RATING:
                message = "What is the new audience rating of the movie?"
                message += "\nPress Enter to skip"
                message += "\nValid Audience Ratings:"
                for rating in AudienceRating:
                    message += f"\n- {rating}"
            case MovieField.RUNTIME:
                message = "What is the new runtime of the movie in minutes?"
                message += "\nPress Enter to skip"
                message += "\nMust be between 1 and 600 (inclusive)"
            case MovieField.GENRE:
                message = "What are the new genres of the movie? (enter a comma separated list)"
                message += "\nPress Enter to skip"
                message += "\nAvailable genres:"

                # Create the genre list by breaking it into 3 lines
                genres = list(Genre)
                num_lines = 3
                for i in range(num_lines):
                    chunk_size = len(genres) // num_lines
                    start_index = i * chunk_size
                    end_index = i * chunk_size + chunk_size

                    line_genres = genres[start_index:end_index]
                    message += "\n"
                    message += ", ".join(map(lambda g: str(g), line_genres))
            case MovieField.STAR_RATING:
                message = "What is the new star rating of the movie?"
                message += "\nPress Enter to skip"
                message += "\nMust be between 0 and 5 (inclusive)"
            case MovieField.WHERE_TO_WATCH:
                message = "Where can the movie be watched?"
                message += "\nPress Enter to skip"
                message += "\nMax 100 characters"

        return message


class Movie:
    """An object that encapsulates a movie."""

    def __init__(
        self,
        id: int,
        name: str,
        release_year: int | None = None,
        audience_rating: AudienceRating | None = None,
        runtime: int | None = None,
        genre: list[Genre] | None = None,
        star_rating: int | None = None,
        where_to_watch: str | None = None,
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

    @property
    def star_rating_string(self) -> str:
        return f"{ui.FULL_STAR_CHAR * self.star_rating}{ui.EMPTY_STAR_CHAR * (5 - self.star_rating)}"

    @property
    def audience_rating_db(self) -> int:
        """Get the audience rating of this movie that can be stored in a database."""
        if self.audience_rating is None:
            return None

        return self.audience_rating.value

    @property
    def genre_db(self) -> str | None:
        """Get the genres of this movie that can be stored in a database."""
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
            output += f" {self.star_rating_string}"

        return output
