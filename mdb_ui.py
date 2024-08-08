"""The code related to managing the individual pages of the UI."""

from enum import Enum

import mdb_console as console


class Page(Enum):
    """An enum representing the current page of the application."""

    HOME = ""
    HELP = "help"
    ALL_MOVIES = "all_movies"
    SINGLE_MOVIE = "single_movie"


# https://en.wikipedia.org/wiki/Box-drawing_characters
HORIZONTAL_BAR_CHAR = "─"
VERTICAL_BAR_CHAR = "│"
PLUS_BAR_CHAR = "┼"
CORNER_BAR_CHARS = "┌┐└┘"
T_BAR_CHARS = "├┤┬┴"

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
    console.write(2, 1, "Home")


def display_all():
    """Render a list of all of the movies."""
    console.write(2, 1, "All movies")


def display_movie():
    """Render a single movie"s information."""
    console.write(2, 1, f"Movie: {current_movie}")
