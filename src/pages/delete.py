"""The delete page of the UI."""

import mdb_console as console
import mdb_ui as ui
from mdb_commands import Command, commands


class DeletePage(ui.Page):
    """The Delete page of the UI."""

    @staticmethod
    def setup():
        """Initialize the page."""
        commands.append(Command("delete", DeletePage.command_delete))

    def __init__(self):
        """Create a page."""
        super().__init__("Delete", 10, 10)

    @staticmethod
    def command_delete():
        """Go to the delete page."""
        ui.current_page = DeletePage()

    def render(self):
        """Render the page."""
