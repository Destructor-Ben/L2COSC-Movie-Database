"""The search page of the UI."""

import mdb_console as console
import mdb_ui as ui
from mdb_commands import Command, commands


class SearchPage(ui.Page):
    """The Search page of the UI."""

    @staticmethod
    def setup():
        """Initialize the page."""
        commands.append(Command("search", SearchPage.command_search))

    def __init__(self):
        """Create a page."""
        super().__init__("Search", 10, 10)

    @staticmethod
    def command_search():
        """Go to the search page."""
        ui.current_page = SearchPage()

    def render(self):
        """Render the page."""
