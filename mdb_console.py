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
CLEAR_COLOR_SEQUENCE = "[0m"

# Buffer of characters
buffer = []

# Buffer of foreground and background colours
# tuple[int, int, int] (rgb values)
# If a characters colour is set to none, then it uses the default colour
fg_colours = []
bg_colours = []

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
    global fg_colours
    global bg_colours
    global width
    global height

    size = get_size()
    width = size[0]
    height = size[1]
    buffer = [[" " for y in range(height)] for x in range(width)]
    fg_colours = [[None for y in range(height)] for x in range(width)]
    bg_colours = [[None for y in range(height)] for x in range(width)]


def set_text_colour(
        current_colour: tuple[int, int, int] | None,
        colour: tuple[int, int, int] | None,
        is_foreground: bool = True):
    """Set the text colour of the console."""
    if (current_colour == colour):
        # Return original if nothing changed
        return current_colour

    # If the intended colour is different to the actual colour, then change it
    if (colour is None):
        # Reset to default
        print_escape_sequence(f"[{39 if is_foreground else 49}m")
    else:
        print_escape_sequence(f"[{38 if is_foreground else 48};2;{colour[0]};{colour[1]};{colour[2]}m")

    # Return new colour
    return colour


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
    current_fg_colour = None
    current_bg_colour = None

    for y in range(height):
        for x in range(width):
            fg_colour = fg_colours[x][y]
            bg_colour = bg_colours[x][y]

            current_fg_colour = set_text_colour(current_fg_colour, fg_colour, True)
            current_bg_colour = set_text_colour(current_bg_colour, bg_colour, False)

            print(buffer[x][y], end="", flush=False)

        # Newline
        # Even though the buffer will overflow to the next line normally,
        # the console can be resized which will affect how it overflows
        print("", flush=False)

    # Clear the colour
    print_escape_sequence(CLEAR_COLOR_SEQUENCE)

    # Flush the buffer and print a cursor so the user can give input
    print(" > ", end="", flush=True)
    user_input = input()

    return True


def set(
        x: int,
        y: int,
        char: chr,
        fg_colour: tuple[int, int, int] | None = None,
        bg_colour: tuple[int, int, int] | None = None):
    """Write the given character to the buffer at the given coordinate."""
    if (x >= width or y >= height):
        return

    buffer[x][y] = char
    fg_colours[x][y] = fg_colour
    bg_colours[x][y] = bg_colour


def write(
        x: int,
        y: int,
        text: str,
        fg_colour: tuple[int, int, int] | None = None,
        bg_colour: tuple[int, int, int] | None = None):
    """Write the given text to the buffer at the given coordinate."""
    for i, char in enumerate(text):
        set(x + i, y, char, fg_colour, bg_colour)
