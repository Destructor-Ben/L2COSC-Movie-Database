"""The code related to managing the individual pages of the UI."""

import enum

import mdb_console as console
import mdb_commands as commands
import mdb_database as db


class Page(enum.Enum):
    """An enum representing the current page of the application."""

    HOME = enum.auto()
    ALL_MOVIES = enum.auto()
    SINGLE_MOVIE = enum.auto()
    SEARCH_RESULTS = enum.auto()
    EDIT_MOVIE = enum.auto()
    DELETE_MOVIE = enum.auto()
    RESET_DATABASE = enum.auto()


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
COLOUR_RED = (235, 64, 52)

current_page = Page.HOME
error_message = None

# Used in movie, search, edit, and delete menu
search_query = None
# TODO: current_movie?

# TODO: probably make classes for each page


# region Pages


def page_home():
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
    name_x = logo_x + 9
    name_y = logo_y + 1 + LOGO_HEIGHT
    console.write(name_x, name_y, "Movie Data Base")

    # Draw the list of commands
    command_x = logo_x + LOGO_WIDTH + 1
    command_y = 2

    console.write(command_x, command_y, "Commands", COLOUR_YELLOW)
    command_y += 1

    for command in commands.COMMANDS:
        console.write(command_x, command_y, command.name)
        command_y += 1


def page_all_movies():
    """Render the movie catalogue page."""
    console.write(2, 1, "All movies")


def page_single_movie():
    """Render the single movie page."""
    console.write(2, 1, "Single Movie")


def page_search_results():
    """Render the search page."""
    console.write(2, 1, "Search Results")


def page_edit_movie():
    """Render the edit page."""
    console.write(2, 1, "Edit Movie")


def page_delete_movie():
    """Render the delete page."""
    console.write(2, 1, "Delete movie")


def page_reset_database():
    """Render the reset database page."""
    console.write(2, 1, "RESET DATABASE")
    # TODO: make a verification for this
    db.reset()


PAGES = {
    Page.HOME: page_home,
    Page.ALL_MOVIES: page_all_movies,
    Page.SINGLE_MOVIE: page_single_movie,
    Page.SEARCH_RESULTS: page_search_results,
    Page.EDIT_MOVIE: page_edit_movie,
    Page.DELETE_MOVIE: page_delete_movie,
    Page.RESET_DATABASE: page_reset_database,
}

# endregion


def render_current_page():
    """Render the current page of the UI."""
    global current_page
    global error_message

    handle_commands()

    # Stop rendering if we exited
    if not console.is_running:
        return

    # Render the UI
    render_common_ui()
    PAGES[current_page]()

    # Reset state
    error_message = None


def handle_commands():
    """Handle commands."""
    global error_message

    # Return if there is no user input
    if console.user_input is None:
        return

    # Remove spaces at the end and beginning and split into args (that aren't empty)
    command = console.user_input.strip().split()

    # Return if there is nothing of value that was inputted
    if len(command) <= 0:
        error_message = "No command provided"
        return

    # Get command info
    command_name = command[0].lower()
    command_args = command[1:]

    # Invoke the command
    command = commands.find(command_name)
    if command is not None:
        command.invoke(command_args)
    else:
        error_message = f"Invalid command: '{console.user_input}'"


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

    # Draw the error message
    if error_message is None:
        return

    error_x = 2
    error_y = -2
    console.write(error_x, error_y, f"Error: {error_message}", COLOUR_RED)
