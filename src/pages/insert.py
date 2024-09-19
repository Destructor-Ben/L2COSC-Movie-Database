"""The insert page of the UI."""

# TODO: implement - This won't have any args in the command

import mdb_console as console
import mdb_database as db
import mdb_ui as ui
from mdb_commands import Command, commands
from mdb_movie import Movie


class InsertPage(ui.Page):
    """The insert page of the UI."""

    ATTRIBUTES = [
        "name",
        "release year",
        "audience rating",
        "runtime",
        "genre",
        "star rating",
        "where to watch",
    ]

    @staticmethod
    def setup():
        """Initialize the page."""
        commands.append(Command("insert", InsertPage.command_insert))

    def __init__(self):
        """Create a page."""
        super().__init__("Insert", 10, 10)
        self.getting_input = True
        self.current_attribute = -1
        self.movie_attributes = []

    @staticmethod
    def command_insert():
        """Go to the insert page."""
        ui.current_page = InsertPage()

    def render(self):
        """Render the page."""
        # If we just asked the user for input, add it
        if self.current_attribute > -1:
            # TODO: validate the input
            self.movie_attributes.append(console.user_input)

        # Get the next attribute for the movie
        self.current_attribute += 1

        # Add the movie if we have reached the end, otherwise ask for the next one
        if self.current_attribute >= len(InsertPage.ATTRIBUTES):
            # TODO: add the movie then get it to be displayed, since the ID will change
            movie = Movie(0, *self.movie_attributes)
            db.insert(movie)
            message = f"Movie successfully added: {movie}"
            self.getting_input = False
        else:
            message = f"What is the {InsertPage.ATTRIBUTES[self.current_attribute]} of the movie?"

        # Write message
        console.write(2, 2, message, ui.COLOUR_BLUE)
