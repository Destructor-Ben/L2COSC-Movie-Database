"""The insert page of the UI."""

# TODO: implement

import mdb_console as console
import mdb_ui as ui
from mdb_commands import Command, commands


class InsertPage(ui.Page):
    """The insert page of the UI."""

    @staticmethod
    def setup():
        """Initialize the page."""
        commands.append(Command("insert", InsertPage.command_insert))

    def __init__(self):
        """Create a page."""
        super().__init__("Insert", 10, 10)

    @staticmethod
    def command_insert():
        """Go to the insert page."""
        ui.current_page = InsertPage()

    def render(self):
        """Render the page."""
