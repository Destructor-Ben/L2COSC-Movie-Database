"""The code related to managing the TUI.

Based on https://stackoverflow.com/questions/2084508/clear-the-terminal-in-python,
as well as https://en.wikipedia.org/wiki/ANSI_escape_code
and https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences.

Note that the buffer has (0, 0) at the TOP LEFT of the terminal.
Unfortunately, it doesn't properly handle resizing until the UI is rerendered.
I might make it so when the console is resized then the UI will automaatically rerender.
"""

import os

ESCAPE_CHAR = chr(27)

# Buffer of characters
buffer = []

width = 0
height = 0

# Render callback
render = None

# Last user input, used in the UI code
user_input = None


def setup(render_callback):
    """Set up the console utilities.

    Must be called before anything else in this file to guarantee proper functionality.
    """
    # Set the callback - Whenever the user enters input or resizes the terminal, the UI must refresh
    global render
    render = render_callback

    # Windows is weird and needs these commands to be run to make ANSI escape codes work
    if (os.name == "nt"):
        os.system("cls")
        os.system("color")


def run():
    """Run the console UI."""
    # We loop until the display function returns false, which will only happen if the renderer returns false
    while display():
        continue


def print_escape_sequence(sequence: str):
    """Print the given escape sequence to the console."""
    print(f"{ESCAPE_CHAR}{sequence}", end="")


def clear():
    """Clear the console."""
    print_escape_sequence("c")


def get_size() -> tuple[int, int]:
    """Get the size of the console."""
    size = os.get_terminal_size()

    # Subtract 1 so we can have room for user input
    return (size.columns, size.lines - 1)


def recreate_buffer():
    """Recreate the screen buffer and clear it."""
    global buffer
    global width
    global height

    size = get_size()
    width = size[0]
    height = size[1]
    buffer = [[" " for y in range(height)] for x in range(width)]


def display() -> bool:
    """Render the UI, display the buffer to the screen, then clear it afterwards.

    Returns whether the app should continue to run.
    """
    global user_input

    # Clear the screen and render the buffer
    clear()
    recreate_buffer()
    should_run = render()
    if (not should_run):
        return False

    # Display buffer contents
    for y in range(height):
        for x in range(width):
            print(buffer[x][y], end="", flush=False)

        # Newline
        # Even though the buffer will overflow to the next line normally,
        # the console can be resized which will affect how it overflows
        print("", flush=False)

    # Flush the buffer and print a cursor so the user can give input
    print(" > ", end="", flush=True)
    user_input = input()

    return True
