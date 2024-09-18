"""The edit page of the UI."""

# TODO: implement - the only arg will be the movie id

import mdb_console as console
import mdb_ui as ui
from mdb_commands import Command, commands


class EditPage(ui.Page):
    """The edit page of the UI."""

    @staticmethod
    def setup():
        """Initialize the page."""
        commands.append(Command("edit", EditPage.command_edit))

    def __init__(self):
        """Create a page."""
        super().__init__("Edit", 10, 10)

    @staticmethod
    def command_edit():
        """Go to the edit page."""
        ui.current_page = EditPage()

    def render(self):
        """Render the page."""
