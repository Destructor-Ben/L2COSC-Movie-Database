"""The movie list page of the UI."""

import mdb_console as console
import mdb_database as db
import mdb_ui as ui
from mdb_commands import Command, commands


class AllMoviesPage(ui.Page):
    """The movie list page of the UI."""

    @staticmethod
    def setup():
        """Initialize the page."""
        commands.append(Command("movies", AllMoviesPage.command_movies))

    def __init__(self):
        """Create a page."""
        super().__init__("Movie List", 10, 10)
        self.movie_index = 0

        self.commands.append(Command("w", AllMoviesPage.command_up))
        self.commands.append(Command("s", AllMoviesPage.command_down))

    @staticmethod
    def command_movies():
        """Go to the movie list page."""
        ui.current_page = AllMoviesPage()

    @staticmethod
    def command_up():
        """Scroll up the page."""
        ui.current_page.movie_index -= 1

    @staticmethod
    def command_down():
        """Scroll down the page."""
        ui.current_page.movie_index += 1

    def render(self):
        """Render the page."""
        # Get the movies
        movies = db.get_all()
        num_movies = len(movies)

        # Calculate various values
        padding = 3
        number_of_rows = console.height - padding * 2
        if self.error_message is None:
            number_of_rows += 1

        # Clamp the movie index
        if self.movie_index < 0:
            self.movie_index = 0

        max_index = num_movies - number_of_rows

        # Also need to clamp the max index, since if there are more rows than movies, it goes negative
        if max_index < 0:
            max_index = 0

        if self.movie_index > max_index:
            self.movie_index = max_index

        # Draw the list
        movie_y = padding
        for i in range(self.movie_index, num_movies):
            # Subtract the first value in the range to get a 0 based index of what is actually shown on screen
            index_drawn_in_list = i - self.movie_index
            if index_drawn_in_list >= number_of_rows:
                break

            # Exit the loop if we have gone too far
            if i >= num_movies:
                break

            # Draw
            console.write(2, movie_y, str(movies[i]))
            movie_y += 1
