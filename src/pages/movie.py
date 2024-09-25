"""The movie page of the UI."""

import mdb_console as console
import mdb_database as db
import mdb_ui as ui
from mdb_commands import Command, commands, get_available_commands
from mdb_movie import MovieField, Movie


class MoviePage(ui.Page):
    """The movie page of the UI."""

    @staticmethod
    def setup():
        """Initialize the page."""
        commands.append(Command("movie", MoviePage.command_movie))

    def __init__(self, movie_id):
        """Create a page."""
        super().__init__("Movie", 10, 10)
        self.movie_id = movie_id
        self.movie = db.get(movie_id)

    @staticmethod
    def command_movie(movie_id):
        """Go to the movie page."""
        ui.current_page = MoviePage(movie_id)

    def render(self):
        """Render the page."""
        # Check if the movie actually exists
        if self.movie is None:
            self.error_message = f"A movie with an ID of '{self.movie_id}' doesn't exist"
            return

        # Make a list of the fields
        fields = [["ID", str(self.movie.id)]]

        if self.movie.release_year is not None:
            fields.append(["Release Year", str(self.movie.release_year)])

        if self.movie.audience_rating is not None:
            fields.append(["Audience Rating", str(self.movie.audience_rating)])

        if self.movie.runtime is not None:
            fields.append(["Runtime", str(self.movie.runtime) + "m"])

        if self.movie.genre is not None:
            fields.append(["Genres", ", ".join(map(lambda g: str(g), self.movie.genre))])

        if self.movie.star_rating is not None:
            fields.append(["Star Rating", str(self.movie.star_rating_string)])

        if self.movie.where_to_watch is not None:
            fields.append(["Where to Watch", str(self.movie.where_to_watch)])

        # Calculate the heifhr of the panel - width of the borders, 7 fields, and the name + a gap
        height = 2 + len(fields) + 2

        # Calculate the width of the panel
        # This is the longest of the fields and the movie name
        width = len(self.movie.name)

        for field in fields:
            field_width = len(f"{field[0]}: {field[1]}")
            if field_width > width:
                width = field_width

        # Align the fields
        for field in fields:
            field_width = len(f"{field[0]}: {field[1]}")
            field[1] = (width - field_width) * " " + field[1]

        # Add 2 to the width for the border and another 2 for padding
        width += 4

        # Calculate the width of the command panel
        command_x = 0
        commands_list = get_available_commands()
        if len(commands_list) > 0:
            # Calculate the widest command and add padding
            widest_command = max([len(str(command)) for command in commands_list + ["Commands"]])
            widest_command += 2
            command_x = -widest_command

        # Calculate the x and y position
        x = (console.width - width + command_x) // 2
        y = (console.height - height) // 2

        # Draw a border
        for border_x in range(width):
            console.set(x + border_x, y, ui.HORIZONTAL_BAR_CHAR)
            console.set(x + border_x, y + height - 1, ui.HORIZONTAL_BAR_CHAR)

        for border_y in range(height):
            console.set(x, y + border_y, ui.VERTICAL_BAR_CHAR)
            console.set(x + width - 1, y + border_y, ui.VERTICAL_BAR_CHAR)

        console.set(x, y, ui.CORNER_BAR_CHARS[0])
        console.set(x + width - 1, y, ui.CORNER_BAR_CHARS[1])
        console.set(x, y + height - 1, ui.CORNER_BAR_CHARS[2])
        console.set(x + width - 1, y + height - 1, ui.CORNER_BAR_CHARS[3])

        # Shift the fields down and right
        x += 2
        y += 1

        # Name and blank gap
        name = self.movie.name
        name_x_offset = (width - len(name) - 2) // 2
        console.write(x + name_x_offset, y, name, ui.COLOUR_GREEN)
        y += 2

        # Rest of the fields
        for field in fields:
            prefix = f"{field[0]}: "
            console.write(x, y, prefix, ui.COLOUR_BLUE)
            console.write(x + len(prefix), y, field[1])
            y += 1
