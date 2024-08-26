import inspect

import mdb_console as console
import mdb_ui as ui

class Command:
    # TODO: make these private
    name: str | None = None
    action = None
    arg_count = 0


    def __init__(self, name: str, action: callable) -> None:
        self.name = name
        self.action = action

        # Automatically figure out how many args there are
        self.arg_count = len(inspect.signature(action).parameters)


    def invoke(self, args):
        if (len(args) != self.arg_count):
            ui.error_message = f"Incorrect argument count ({len(args)} instead of {self.arg_count})"
            return

        self.action(*args)


def command_exit():
    """Exit the application."""
    console.is_running = False


def command_home():
    """Go to the home page."""
    ui.current_page = ui.Page.HOME


def command_movie(movie_name):
    """Go to the movie page."""
    if (movie_name == "all"):
        ui.current_page = ui.Page.ALL_MOVIES
    else:
        ui.current_page = ui.Page.SINGLE_MOVIE
        ui.search_query = movie_name


def command_search(query):
    """Go to the search page."""
    ui.current_page = ui.Page.SEARCH_RESULTS
    ui.search_query = query


def command_edit():
    """Go to the edit page."""
    ui.current_page = ui.Page.EDIT_MOVIE


def command_delete():
    """Go to the delete page."""
    ui.current_page = ui.Page.DELETE_MOVIE


def command_reset():
    """Go to the reset page."""
    ui.current_page = ui.Page.RESET_DATABASE


# List of commands
COMMANDS = [
    Command("exit",   command_exit),
    Command("home",   command_home),
    Command("movie",  command_movie),
    Command("search", command_search),
    Command("edit",   command_edit),
    Command("delete", command_delete),
    Command("reset",  command_reset),
]


def find(name: str) -> Command | None:
    """Find a command with the given name."""
    for command in COMMANDS:
        if (command.name == name):
            return command

    return None
