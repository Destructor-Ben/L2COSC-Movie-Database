"""The movie page of the UI."""

import mdb_console as console
import mdb_database as db
import mdb_ui as ui
from mdb_commands import Command, commands


# TODO: improve this
class MoviePage(ui.Page):
    """The movie page of the UI."""

    @staticmethod
    def setup():
        """Initialize the page."""
        commands.append(Command("movie", MoviePage.command_movie))

    def __init__(self, movie_id):
        """Create a page."""
        super().__init__("Movie", 10, 10)
        self.movie_id = movie_id
        self.movie = db.get(movie_id)

    @staticmethod
    def command_movie(movie_id):
        """Go to the movie page."""
        ui.current_page = MoviePage(movie_id)

    def render(self):
        """Render the page."""
        # Check if the movie actually exists
        if self.movie is None:
            self.error_message = f"A movie with an ID of '{self.movie_id}' doesn't exist"
            return

        # Draw the movie info
        x = 2
        y = 2

        console.write(x, y, self.movie.id)
        y += 1
        console.write(x, y, self.movie.name)
        y += 1
        console.write(x, y, self.movie.release_year)
        y += 1
        console.write(x, y, self.movie.audience_rating)
        y += 1
        console.write(x, y, self.movie.runtime)
        y += 1
        console.write(x, y, ", ".join(map(lambda g: str(g), self.movie.genre)))
        y += 1
        console.write(x, y, self.movie.star_rating)
        y += 1
        console.write(x, y, self.movie.where_to_watch)
        y += 1
