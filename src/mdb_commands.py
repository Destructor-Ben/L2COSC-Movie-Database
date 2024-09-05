"""The code related to commands."""

# TODO: make all commands in their own files and be oop based

import inspect

import mdb_console as console
import mdb_ui as ui


class Command:
    """An enscapsulation of a command."""

    def __init__(self, name: str, action: callable) -> None:
        """Create a command with a name and an action."""
        self._name = name
        self._action = action

        # Automatically figure out how many args there are
        self._arg_count = len(inspect.signature(action).parameters)

    @property
    def name(self):
        """The name of the command."""
        return self._name

    @property
    def action(self):
        """The action of the command."""
        return self._action

    @property
    def arg_count(self):
        """The number of arguments of the command."""
        return self._arg_count

    def invoke(self, args):
        """Run the command with the given arguments."""
        if len(args) != self.arg_count:
            ui.current_page.error_message = f"Incorrect argument count ({len(args)} instead of {self.arg_count})"
            return

        self.action(*args)


def command_exit():
    """Exit the application."""
    console.is_running = False


def command_home():
    """Go to the home page."""
    ui.current_page = ui.HomePage()


def command_movie(movie_name):
    """Go to the movie page."""
    ui.current_page = ui.MoviePage()


def command_movies():
    """Go to the movie list page."""
    ui.current_page = ui.AllMoviesPage()


def command_search():
    """Go to the search page."""
    ui.current_page = ui.SearchPage()


def command_edit():
    """Go to the edit page."""
    ui.current_page = ui.EditPage()


def command_delete():
    """Go to the delete page."""
    ui.current_page = ui.DeletePage()


def command_reset():
    """Go to the reset page."""
    ui.current_page = ui.ResetPage()


# List of commands
commands = [
    Command("exit", command_exit),
    Command("home", command_home),
    Command("movie", command_movie),
    Command("movies", command_movies),
    Command("search", command_search),
    Command("edit", command_edit),
    Command("delete", command_delete),
    Command("reset", command_reset),
]


def find(name: str) -> Command | None:
    """Find a command with the given name."""
    for command in get_available_commands():
        if command.name.lower() == name.lower():
            return command

    return None


def get_available_commands() -> list[Command]:
    return commands + ui.current_page.commands
