"""The code related to managing the individual pages of the UI."""

# TODO: put all pages in their own files

import mdb_commands as commands
import mdb_console as console
import mdb_database as db

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
        pass

# region Pages


class MoviePage(Page):
    """The movie info page of the UI."""

    def __init__(self):
        """Create a page."""
        super().__init__("Movie", 10, 10)

    def render(self):
        """Render the page."""
        pass


class SearchPage(Page):
    """The search page of the UI."""

    def __init__(self):
        """Create a page."""
        super().__init__("Search", 10, 10)

    def render(self):
        """Render the page."""
        pass


class EditPage(Page):
    """The edit page of the UI."""

    def __init__(self):
        """Create a page."""
        super().__init__("Edit", 10, 10)

    def render(self):
        """Render the page."""
        pass


class DeletePage(Page):
    """The delete page of the UI."""

    def __init__(self):
        """Create a page."""
        super().__init__("Delete", 10, 10)

    def render(self):
        """Render the page."""
        pass


class ResetPage(Page):
    """The reset page of the UI."""

    def __init__(self):
        """Create a page."""
        super().__init__("Reset", 10, 10)

    def render(self):
        """Render the page."""
        db.reset()


# endregion

current_page: Page = None


def init_pages():
    """Initialize the pages."""
    # Only import them here since otherwise it causes a crash because the Page object doesn't exist yet
    import pages.home
    import pages.movies

    # Static page init
    pages.home.HomePage.setup()
    pages.movies.AllMoviesPage.setup()

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
    render_common_ui()
    current_page.render()

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
    if current_page.error_message is None:
        return

    console.write(2, -2, f"Error: {current_page.error_message}", COLOUR_RED)
