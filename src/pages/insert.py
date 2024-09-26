"""The insert page of the UI."""

import mdb_console as console
import mdb_database as db
import mdb_ui as ui
from mdb_commands import Command, commands
from mdb_movie import MovieField, Movie


class InsertPage(ui.Page):
    """The insert page of the UI."""

    MOVIE_FIELDS = [
        MovieField.NAME,
        MovieField.RELEASE_YEAR,
        MovieField.AUDIENCE_RATING,
        MovieField.RUNTIME,
        MovieField.GENRE,
        MovieField.STAR_RATING,
        MovieField.WHERE_TO_WATCH,
    ]

    @staticmethod
    def setup():
        """Initialize the page."""
        commands.append(Command("insert", InsertPage.command_insert))

    def __init__(self):
        """Create a page."""
        super().__init__("Insert")
        self.getting_input = True
        # The index in MOVIE_FIELDS we are currently searching for
        self.current_field_index = 0
        # Dictionary of all of the movie fields
        self.movie_fields = {}
        # Used to render the final page
        self.movie_added = False
        self.movie = None
        # Stops us wrongly using "insert" as the initial user input
        self.first_open = True
        # Make sure the name is enforced
        self.enforce_name = True

    @staticmethod
    def command_insert():
        """Go to the insert page."""
        ui.current_page = InsertPage()

    @property
    def current_field(self) -> MovieField:
        """Get the enum for current field the user is inputting."""
        return InsertPage.MOVIE_FIELDS[self.current_field_index]

    def on_finish_input(self):
        """Add the movie to the database once the user is done giving input."""
        # Add the movie
        movie = Movie(0, *self.movie_fields.values())
        movie_id = db.insert(movie)

        # Get the movie (with the updated ID from inserting it)
        self.getting_input = False
        self.movie_added = True
        self.movie = db.get(movie_id)

    def get_prompt(self):
        """Get the prompt for the user for the given movie field."""
        return self.current_field.get_insert_prompt()

    def get_complete_message(self) -> str:
        """Get the message to be displayed when the movie is added."""
        return "Movie successfully added:"

    def handle_input(self):
        """Handle the page's input."""
        # Don't use input if the user hasn't even been prompted yet
        # Also don't handle input if the movie has been added already
        if self.first_open or self.movie_added:
            return

        # If we just asked the user for input, get it and validate it
        # Validate the input
        (is_valid, user_input, error_message) = self.current_field.validate_field(console.user_input.strip(), self.enforce_name)

        # Return if it isn't valid
        if is_valid == False:
            self.error_message = error_message
            return

        # Add the field
        self.movie_fields[self.current_field] = user_input

        # Get the next field for the movie
        self.current_field_index += 1
        
        # Add the movie if we have reached the end of the required fields
        if self.current_field_index >= len(InsertPage.MOVIE_FIELDS):
            self.on_finish_input()

    def render(self):
        """Render the page."""
        message_x = 2
        message_y = 2

        self.handle_input()

        # This is used to stop the input from running on the "insert" command
        if self.first_open:
            self.first_open = False

        # Draw the info showing the after it is added
        if self.movie_added:
            console.write(message_x, message_y, self.get_complete_message(), ui.COLOUR_BLUE)
            console.write(message_x, message_y + 1, self.movie)
            return

        # Draw the prompt for the user
        message = self.get_prompt()
        for line in message.split("\n"):
            console.write(message_x, message_y, line, ui.COLOUR_BLUE)
            message_y += 1
