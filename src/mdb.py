"""The main file for MDB."""

import mdb_console as console
import mdb_database as db
import mdb_ui as ui

if __name__ == "__main__":
    db.setup()
    ui.init_pages()
    console.setup(ui.render_current_page)
    console.run()
