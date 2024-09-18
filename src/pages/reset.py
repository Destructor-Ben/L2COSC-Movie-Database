"""The reset page of the UI."""

import mdb_console as console
import mdb_database as db
import mdb_ui as ui
from mdb_commands import Command, commands


class ResetPage(ui.Page):
    """The reset page of the UI."""

    @staticmethod
    def setup():
        """Initialize the page."""
        commands.append(Command("reset", ResetPage.command_reset))

    def __init__(self):
        """Create a page."""
        super().__init__("Reset", 10, 10)
        self.global_commands_available = False
        self.commands.append(Command("yes", ResetPage.command_yes))
        self.commands.append(Command("no", ResetPage.command_no))
        self.database_reset = None

    @staticmethod
    def command_reset():
        """Go to the reset page."""
        ui.current_page = ResetPage()

    @staticmethod
    def command_yes():
        """Called when the user enters "no"."""
        db.reset()
        ui.current_page.database_reset = True

        # Allow the user to leave
        ui.current_page.global_commands_available = True
        ui.current_page.commands.clear()

    @staticmethod
    def command_no():
        """Called when the user enters "no"."""
        ui.current_page.database_reset = False

        # Allow the user to leave
        ui.current_page.global_commands_available = True
        ui.current_page.commands.clear()

    def render(self):
        """Render the page."""
        message_x = 2
        message_y = 2

        # Write a message so the user knows whats happening
        if self.database_reset is None:
            console.write(message_x, message_y, "Are you sure you want to reset the database?", ui.COLOUR_RED)
        elif self.database_reset:
            console.write(message_x, message_y, "The database was reset", ui.COLOUR_RED)
        else:
            console.write(message_x, message_y, "The database was not reset", ui.COLOUR_BLUE)
