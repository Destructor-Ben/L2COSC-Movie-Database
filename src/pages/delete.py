"""The delete page of the UI."""

import mdb_console as console
import mdb_database as db
import mdb_ui as ui
from mdb_commands import Command, commands


class DeletePage(ui.Page):
    """The delete page of the UI."""

    @staticmethod
    def setup():
        """Initialize the page."""
        commands.append(Command("delete", DeletePage.command_delete))

    def __init__(self, movie_id):
        """Create a page."""
        super().__init__("Delete")
        self.movie_id = movie_id

        self.global_commands_available = False
        self.commands.append(Command("yes", DeletePage.command_yes))
        self.commands.append(Command("no", DeletePage.command_no))
        self.movie_deleted = None

    @staticmethod
    def command_delete(movie_id):
        """Go to the delete page."""
        if db.get(movie_id) is None:
            ui.current_page.error_message = f"Invalid movie id ({movie_id})"
            return

        ui.current_page = DeletePage(movie_id)

    @staticmethod
    def command_yes():
        """Call when the user enters "no"."""
        db.delete(ui.current_page.movie_id)
        ui.current_page.movie_deleted = True

        # Allow the user to leave
        ui.current_page.global_commands_available = True
        ui.current_page.commands.clear()

    @staticmethod
    def command_no():
        """Call when the user enters "no"."""
        ui.current_page.movie_deleted = False

        # Allow the user to leave
        ui.current_page.global_commands_available = True
        ui.current_page.commands.clear()

    def render(self):
        """Render the page."""
        message_x = 2
        message_y = 2

        # Write a message so the user knows whats happening
        movie = db.get(self.movie_id)
        if self.movie_deleted is None:
            console.write(message_x, message_y, "Are you sure you want to delete the movie?", ui.COLOUR_RED)
            message_y += 1
            console.write(message_x, message_y, movie, ui.COLOUR_BLUE)
        elif self.movie_deleted:
            console.write(message_x, message_y, "The movie was deleted", ui.COLOUR_RED)
        else:
            console.write(message_x, message_y, "The movie was not deleted", ui.COLOUR_BLUE)
