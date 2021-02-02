import os
import time
from pathlib import Path

from S3_File_Uploader.UI.ProgramController import ProgramController


def remove_db_file():
    # Get the full path to where the database file is located.
    db_file_path = os.path.join(Path(__file__).parents[2], 'db.sqlite3')

    if os.path.exists(db_file_path):
        os.remove(db_file_path)


def update_program_controller_loop(program_controller: ProgramController, seconds: int = 1) -> None:
    """ Run a loop for the guiven seconds that updates idle tasks and user input tasks.
    This function needs to be used because to be able to test Tkinter UI elements , the test
    cannot use the mainloop function of tkinter. That means that Tkinter needs to be updated manually.

    Args:
        seconds (int, optional): Seconds to run the loop. Defaults to 1.
            Each second, the update and update_idletasks functions run around 2600 times (depending on CPU clock speed).
    """

    secs = seconds
    start_time = time.time()
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time

        if elapsed_time < secs:
            program_controller.update_idletasks()
            program_controller.update()
        else:
            break
