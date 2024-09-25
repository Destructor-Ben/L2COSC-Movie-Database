"""The edit page of the UI."""

# TODO: implement - the only arg will be the movie id
# Base this off the insert page

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
        super().__init__("Edit")

    @staticmethod
    def command_edit(movie_id):
        """Go to the edit page."""
        ui.current_page = EditPage()

    def render(self):
        """Render the page."""
        console.write(2, 2, "SIGMA")
