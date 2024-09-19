"""The search page of the UI."""

import mdb_database as db
import mdb_ui as ui
from pages.movies import AllMoviesPage
from mdb_commands import Command, commands


# The code for this is basically the same as the movie list, so we copy it
class SearchPage(AllMoviesPage):
    """The search page of the UI."""

    ATTRIBUTES = [
        "name",
        "release_year",
        "audience_rating",
        "runtime",
        "genre",
        "star_rating",
        "where_to_watch",
    ]

    @staticmethod
    def setup():
        """Initialize the page."""
        commands.append(Command("search", SearchPage.command_search))

    def __init__(self, attribute, query):
        """Create a page."""
        super().__init__()
        self.name = "Search"
        self.attribute = attribute
        self.query = query

    @staticmethod
    def command_search(attribute, query):
        """Go to the search page."""
        #if attribute.lower().strip() not in SearchPage.ATTRIBUTES:
            #ui.current_page.error_message = f"Invalid attribute ({attribute})"
            #return

        # TODO: validate query

        ui.current_page = SearchPage(attribute, query)

    def get_movies(self):
        return db.get_filter(self.attribute, self.query)
