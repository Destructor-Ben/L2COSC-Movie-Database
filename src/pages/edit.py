"""The edit page of the UI."""

import mdb_database as db
import mdb_ui as ui
from mdb_movie import MovieField
from mdb_commands import Command, commands
from pages.insert import InsertPage

# TODO: don't force the name to get edited


class EditPage(InsertPage):
    """The edit page of the UI."""

    @staticmethod
    def setup():
        """Initialize the page."""
        commands.append(Command("edit", EditPage.command_edit))

    def __init__(self, movie):
        """Create a page."""
        super().__init__()
        self.name = "Edit"
        self.movie = movie
        # Don't force the user to edit the name
        self.enforce_name = False

    def on_finish_input(self):
        """Add the movie to the database once the user is done giving input."""
        # Edit the movie
        movie = self.movie

        name = self.movie_fields[MovieField.NAME]
        if name is not None:
            movie.name = name

        release_year = self.movie_fields[MovieField.RELEASE_YEAR]
        if release_year is not None:
            movie.release_year = release_year

        audience_rating = self.movie_fields[MovieField.AUDIENCE_RATING]
        if audience_rating is not None:
            movie.audience_rating = audience_rating

        runtime = self.movie_fields[MovieField.RUNTIME]
        if runtime is not None:
            movie.runtime = runtime

        genre = self.movie_fields[MovieField.GENRE]
        if genre is not None:
            movie.genre = genre

        star_rating = self.movie_fields[MovieField.STAR_RATING]
        if star_rating is not None:
            movie.star_rating = star_rating

        where_to_watch = self.movie_fields[MovieField.WHERE_TO_WATCH]
        if where_to_watch is not None:
            movie.where_to_watch = where_to_watch

        db.edit(movie)
        movie_id = movie.id

        # Get the movie (to ensure it is properly updated)
        self.getting_input = False
        self.movie_added = True
        self.movie = db.get(movie_id)

    def get_prompt(self):
        """Get the prompt for the user for the given movie field."""
        return self.current_field.get_edit_prompt()

    def get_complete_message(self) -> str:
        """Get the message to be displayed when the movie is added."""
        return "Movie successfully edited:"

    @staticmethod
    def command_edit(movie_id):
        """Go to the edit page."""
        movie = db.get(movie_id)
        if movie is None:
            ui.current_page.error_message = f"Invalid movie id '{movie_id}'"
            return

        ui.current_page = EditPage(movie)
