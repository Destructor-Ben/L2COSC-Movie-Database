"""The movie list page of the UI."""

import mdb_console as console
import mdb_database as db
import mdb_ui as ui
from mdb_commands import Command, commands


class AllMoviesPage(ui.Page):
    """The movie list page of the UI."""

    PADDING = 3

    @staticmethod
    def setup():
        """Initialize the page."""
        commands.append(Command("movies", AllMoviesPage.command_movies))

    def __init__(self):
        """Create a page."""
        super().__init__("Movie List")
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
        ui.current_page.movie_index -= AllMoviesPage.get_number_of_rows()

    @staticmethod
    def command_down():
        """Scroll down the page."""
        ui.current_page.movie_index += AllMoviesPage.get_number_of_rows()

    @staticmethod
    def get_number_of_rows():
        """Get the number of movies that can be displayed."""
        return console.height - AllMoviesPage.PADDING * 2 - 1

    def get_movies(self):
        """Get the movies to be displayed."""
        return db.get_all()

    def render(self):
        """Render the page."""
        # Write a message to make it clear on how to use it
        console.write(2, 2, "Type 'w' or 's' and press enter to scroll up or down", ui.COLOUR_BLUE)

        # Get the movies
        movies = self.get_movies()
        num_movies = len(movies)

        # Calculate various values
        number_of_rows = AllMoviesPage.get_number_of_rows()
        if self.error_message is None:
            number_of_rows += 1

        # Clamp the movie index
        if self.movie_index < 0:
            self.movie_index = 0

        max_index = num_movies - number_of_rows
        max_index += 1  # Add 1 for the end of list indicator

        # Also need to clamp the max index, since if there are more rows than movies, it goes negative
        if max_index < 0:
            max_index = 0

        if self.movie_index > max_index:
            self.movie_index = max_index

        # Calculate the padding - 1 addded for the message about how to scroll
        movie_y = AllMoviesPage.PADDING + 1

        # Draw the empty list indicator
        if num_movies <= 0:
            console.write(2, movie_y, "No movies found", ui.COLOUR_RED)
            return

        # Draw the list - 1 added for the end of list indicator
        for i in range(self.movie_index, num_movies + 1):
            # Subtract the first value in the range to get a 0 based index of what is actually shown on screen
            index_drawn_in_list = i - self.movie_index
            if index_drawn_in_list >= number_of_rows:
                break

            # Exit the loop if we have gone too far
            if i > num_movies:
                break

            # End of list indicator
            if i == num_movies:
                text = "[End of list]"
            else:
                text = movies[i]

            # Draw
            console.write(2, movie_y, text)
            movie_y += 1
