"""The code related to commands."""

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


# List of commands
commands = [
    Command("exit", command_exit),
]


def find(name: str) -> Command | None:
    """Find a command with the given name."""
    for command in get_available_commands():
        if command.name.lower() == name.lower():
            return command

    return None


def get_available_commands() -> list[Command]:
    """Get a list of the available commands."""
    return commands + ui.current_page.commands
