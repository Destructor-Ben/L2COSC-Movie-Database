"""The search page of the UI."""

import mdb_database as db
import mdb_ui as ui
from pages.movies import AllMoviesPage
from mdb_commands import Command, commands
from mdb_movie import MovieField


# The code for this is basically the same as the movie list, so we copy it
class SearchPage(AllMoviesPage):
    """The search page of the UI."""

    @staticmethod
    def setup():
        """Initialize the page."""
        commands.append(Command("search", SearchPage.command_search))

    def __init__(self, field, query):
        """Create a page."""
        super().__init__()
        self.name = "Search"
        self.field = field
        self.query = query

    @staticmethod
    def command_search(field, query):
        """Go to the search page."""
        # Check that the given movie field exists
        movie_field = MovieField.from_str(field)
        if movie_field is None:
            # TODO: give user feedback for what is a valid field
            ui.current_page.error_message = f"Invalid movie field ({field})"
            return

        # Check that the query itself is valid
        (is_valid, _, error_message) = movie_field.validate_field(query)
        if not is_valid:
            ui.current_page.error_message = f"Invalid movie query ({query}) - {error_message}"
            return

        # Go to the page
        ui.current_page = SearchPage(movie_field, query)

    def get_movies(self):
        """Get the movies to be displayed."""
        return db.get_filter(self.field.database_name, self.query)
