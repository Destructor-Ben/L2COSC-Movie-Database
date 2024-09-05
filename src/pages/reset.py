"""The reset page of the UI."""

import mdb_console as console
import mdb_database as db
import mdb_ui as ui
from mdb_commands import Command, commands


class ResetPage(ui.Page):
    """The Reset page of the UI."""

    @staticmethod
    def setup():
        """Initialize the page."""
        commands.append(Command("reset", ResetPage.command_reset))

    def __init__(self):
        """Create a page."""
        super().__init__("Reset", 10, 10)

    @staticmethod
    def command_reset():
        """Go to the reset page."""
        ui.current_page = ResetPage()

    def render(self):
        """Render the page."""
        # TODO: add confirmation
        db.reset()
