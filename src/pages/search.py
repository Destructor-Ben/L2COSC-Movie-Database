"""The search page of the UI."""

import mdb_database as db
import mdb_ui as ui
from mdb_commands import Command, commands
from mdb_movie import MovieField
from pages.movies import AllMoviesPage


# The code for this is basically the same as the movie list, so we copy it
# TODO: show the query
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
        if movie_field is None or movie_field is MovieField.ID:
            # TODO: give user feedback for what is a valid field - these are too long
            ui.current_page.error_message = f"Invalid movie field '{field}' - Must be name, release_year, audience_rating, runtime, genre, star_rating, or where_to_watch"
            return

        # Check that the query is valid
        (is_valid, parsed_query, error_message) = movie_field.validate_field(query)
        if not is_valid:
            ui.current_page.error_message = f"Invalid movie query '{query}' - {error_message}"
            return

        # Go to the page
        ui.current_page = SearchPage(movie_field, parsed_query)

    def get_movies(self):
        """Get the movies to be displayed."""
        return db.get_filter(self.field, self.query)
