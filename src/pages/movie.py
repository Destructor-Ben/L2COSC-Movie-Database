"""The movie page of the UI."""

import mdb_console as console
import mdb_ui as ui
from mdb_commands import Command, commands


class MoviePage(ui.Page):
    """The Movie page of the UI."""

    @staticmethod
    def setup():
        """Initialize the page."""
        commands.append(Command("movie", MoviePage.command_movie))

    def __init__(self):
        """Create a page."""
        super().__init__("Movie", 10, 10)

    @staticmethod
    def command_movie(movie_name):
        """Go to the movie page."""
        ui.current_page = MoviePage()

    def render(self):
        """Render the page."""
