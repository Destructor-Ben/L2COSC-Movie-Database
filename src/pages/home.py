"""The home page of the UI."""

import mdb_console as console
import mdb_ui as ui
from mdb_commands import Command, commands, get_available_commands


class HomePage(ui.Page):
    """The home page of the UI."""

    @staticmethod
    def setup():
        """Initialize the page."""
        commands.append(Command("home", HomePage.command_home))

    def __init__(self):
        """Create a page."""
        super().__init__("Home", 10, 17)

    @staticmethod
    def command_home():
        """Go to the home page."""
        ui.current_page = HomePage()

    def render(self):
        """Render the page."""
        # Coords of the top left of the logo
        logo_x = 1
        logo_y = 3

        # Draw the logo
        for x in range(ui.LOGO_WIDTH):
            for y in range(ui.LOGO_HEIGHT):
                # Y before X in this because the rows are ordered first
                console.set(logo_x + x, logo_y + y, ui.LOGO[y][x], ui.COLOUR_GREEN)

        # Print name
        name_x = logo_x + 9
        name_y = logo_y + 1 + ui.LOGO_HEIGHT
        console.write(name_x, name_y, "Movie Data Base")

        # Draw the list of commands
        # TODO: make this common ui
        command_x = logo_x + ui.LOGO_WIDTH + 1
        command_y = 2

        console.write(command_x, command_y, "Commands", ui.COLOUR_YELLOW)
        command_y += 1

        for command in get_available_commands():
            console.write(command_x, command_y, command.name)
            command_y += 1
