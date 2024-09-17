"""The code related to managing the individual pages of the UI."""

# TODO: finish UI

import mdb_commands as commands
import mdb_console as console

# Made from https://patorjk.com/software/taag/#p=display&f=Slant%20Relief&t=MDB
# Made pretty with this: https://stackoverflow.com/questions/10660435/how-do-i-split-the-definition-of-a-long-string-over-multiple-lines
LOGO = (
    r" /\\\\            /\\\\  /\\\\\\\\\\\\     /\\\\\\\\\\\\\         ",
    r" \/\\\\\\        /\\\\\\ \/\\\////////\\\  \/\\\/////////\\\      ",
    r"  \/\\\//\\\    /\\\//\\\ \/\\\      \//\\\ \/\\\       \/\\\     ",
    r"   \/\\\\///\\\/\\\/ \/\\\ \/\\\       \/\\\ \/\\\\\\\\\\\\\\     ",
    r"    \/\\\  \///\\\/   \/\\\ \/\\\       \/\\\ \/\\\/////////\\\   ",
    r"     \/\\\    \///     \/\\\ \/\\\       \/\\\ \/\\\       \/\\\  ",
    r"      \/\\\             \/\\\ \/\\\       /\\\  \/\\\       \/\\\ ",
    r"       \/\\\             \/\\\ \/\\\\\\\\\\\\/   \/\\\\\\\\\\\\\/ ",
    r"        \///              \///  \////////////     \/////////////  ",
)

LOGO_WIDTH = len(LOGO[0])
LOGO_HEIGHT = len(LOGO)

# https://en.wikipedia.org/wiki/Box-drawing_characters
HORIZONTAL_BAR_CHAR = "─"
VERTICAL_BAR_CHAR = "│"
PLUS_BAR_CHAR = "┼"
CORNER_BAR_CHARS = "┌┐└┘"
T_BAR_CHARS = "├┤┬┴"

FULL_STAR_CHAR = "★"
EMPTY_STAR_CHAR = "☆"
# Sadly, the half star character isn't supported by many fonts so we can't use it
# HALF_STAR_CHAR = "⯨"

COLOUR_GREEN = (43, 255, 100)
COLOUR_YELLOW = (255, 245, 100)
COLOUR_RED = (235, 64, 52)
COLOUR_BLUE = (121, 184, 255)
COLOUR_LIGHT_BLUE = (158, 203, 242)


class Page:
    """An abstract enscapsulation of a page."""

    def __init__(self, name: str, min_width: int, min_height: int):
        """Create a page."""
        # Immutable
        self.name = name
        self.min_width = min_width
        self.min_height = min_height

        # Mutable
        self.error_message = None
        self.global_commands_available = True
        self.commands = []

    def render(self):
        """Render the page."""
        self.error_message = "Page has no render code"


current_page: Page = None


def init_pages():
    """Initialize the pages."""
    # Only import them here since otherwise it causes a crash because the Page object doesn't exist yet
    # Need to disable formatting order since the order of imports matters for the order of commands
    import pages.home  # noqa: I001
    import pages.movie
    import pages.movies
    import pages.search
    import pages.edit
    import pages.delete
    import pages.reset

    # Static page init
    pages.home.HomePage.setup()
    pages.movie.MoviePage.setup()
    pages.movies.AllMoviesPage.setup()
    pages.search.SearchPage.setup()
    pages.edit.EditPage.setup()
    pages.delete.DeletePage.setup()
    pages.reset.ResetPage.setup()

    # Set the default page
    global current_page
    current_page = pages.home.HomePage()


def render_current_page():
    """Render the current page of the UI."""
    handle_commands()

    # Stop rendering if we exited
    if not console.is_running:
        return

    # Check if the console is too small
    if console.width < current_page.min_width or console.height < current_page.min_height:
        size_hint = f"({console.width}x{console.height} instead of {current_page.min_width}x{current_page.min_height})"
        console.write(0, 0, f"Error: Console too small to render page {size_hint}", COLOUR_RED)
        return

    # Render the UI
    current_page.render()
    render_common_ui()

    # Reset stuff
    current_page.error_message = None


def handle_commands():
    """Handle commands."""
    # Return if there is no user input
    if console.user_input is None:
        return

    # Remove spaces at the end and beginning and split into args (that aren't empty)
    command = console.user_input.strip().split()

    # Return if there is nothing of value that was inputted
    if len(command) <= 0:
        current_page.error_message = "No command provided"
        return

    # Get command info
    command_name = command[0].lower()
    command_args = command[1:]

    # Invoke the command
    command = commands.find(command_name)
    if command is not None:
        command.invoke(command_args)
    else:
        current_page.error_message = f"'{console.user_input}' is not a valid command"


def render_common_ui():
    """Render the UI common to all pages."""
    # Draw a border around the window
    for x in range(console.width):
        console.set(x, 0, HORIZONTAL_BAR_CHAR)
        console.set(x, -1, HORIZONTAL_BAR_CHAR)

    for y in range(console.height):
        console.set(0, y, VERTICAL_BAR_CHAR)
        console.set(-1, y, VERTICAL_BAR_CHAR)

    console.set(0, 0, CORNER_BAR_CHARS[0])
    console.set(-1, 0, CORNER_BAR_CHARS[1])
    console.set(0, -1, CORNER_BAR_CHARS[2])
    console.set(-1, -1, CORNER_BAR_CHARS[3])

    # Draw the page name
    console.write(2, 1, current_page.name, COLOUR_YELLOW)

    # Draw the error message
    if current_page.error_message is not None:
        console.write(2, -2, f"Error: {current_page.error_message}", COLOUR_RED)

    # Draw the list of commands
    commands_list = commands.get_available_commands()
    if len(commands_list) <= 0:
        return

    # Calculate the widest command and add padding
    widest_command = max([len(str(command)) for command in commands_list])
    widest_command += 2

    command_x = -widest_command
    command_y = 1

    # Draw the left barrier
    for y in range(console.height):
        console.set(command_x - 2, y, VERTICAL_BAR_CHAR)
    
    console.set(command_x - 2, 0, T_BAR_CHARS[2])
    console.set(command_x - 2, -1, T_BAR_CHARS[3])

    # Header
    console.write(command_x, command_y, "Commands", COLOUR_YELLOW)
    command_y += 2

    # List of commands
    for command in commands_list:
        console.write(command_x, command_y, command, COLOUR_LIGHT_BLUE)
        command_y += 1
