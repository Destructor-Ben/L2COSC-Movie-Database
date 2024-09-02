"""The code for the movie structure that is used in the database."""


class Movie:
    """An object that encapsulates a movie."""

    def __init__(
        self,
        id: int,
        name: str,
        release_year: int = None,
        audience_rating: str = None,
        runtime: int = None,
        genre: list[str] = None,
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
