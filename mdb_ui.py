"""The code related to managing the individual pages of the UI."""

from enum import Enum

import mdb_console as console


class Page(Enum):
    """An enum representing the current page of the application."""

    HOME = ""
    HELP = "help"
    ALL_MOVIES = "all_movies"
    SINGLE_MOVIE = "single_movie"


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

COLOUR_GREEN = (43, 255, 100)
COLOUR_YELLOW = (255, 245, 100)

COMMON_COMMANDS = {
    "help": None
}

PAGES = {
    
}

# TODO: make a dictionary of pages and commands

current_page = Page.HOME
current_movie = None


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

def render_current_page():
    """Render the current page of the UI.

    Returns whether the app should continue to run.
    """
    global current_page

    # Common commands
    # TODO: should this even exist? maybe make this specific to the home page
    user_input = console.user_input
    # TODO: make this a dictionary and add a thing that asks if you meant XX if it"s similar
    command = user_input.lower().strip() if user_input is not None else None
    if (command == "exit"):
        return False
    elif (command == "home"):
        current_page = Page.HOME
    elif (command == "all"):
        current_page = Page.ALL_MOVIES
    elif (command == "movie"):
        current_page = Page.SINGLE_MOVIE

    # Render the UI
    render_common_ui()

    if (current_page == Page.HOME):
        home()
    elif (current_page == Page.ALL_MOVIES):
        display_all()
    elif (current_page == Page.SINGLE_MOVIE):
        display_movie()
    else:
        console.write(2, 1, f"Invalid page: {current_page}")

    return True


def home():
    """Render the home page."""
    # Coords of the top left of the logo
    logo_x = 1
    logo_y = 2

    # Draw the logo
    for x in range(LOGO_WIDTH):
        for y in range(LOGO_HEIGHT):
            # Y before X in this because the rows are ordered first
            console.set(logo_x + x, logo_y + y, LOGO[y][x], COLOUR_GREEN)

    # Print name
    console.write(logo_x + 9, logo_y + 1 + LOGO_HEIGHT, "Movie Data Base")

    # Draw the list of commands
    command_x = logo_x + LOGO_WIDTH + 1
    command_y = 2

    console.write(command_x, command_y, "Commands", COLOUR_YELLOW)
    command_y += 1
    
    for command in COMMON_COMMANDS:
        console.write(command_x, command_y, command)
        command_y += 1


def display_all():
    """Render a list of all of the movies."""
    console.write(2, 1, "All movies")


def display_movie():
    """Render a single movie"s information."""
    console.write(2, 1, f"Movie: {current_movie}")
