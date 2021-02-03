import os
import time

from S3_File_Uploader import DatabasePath
from S3_File_Uploader.UI.ProgramController import ProgramController


def remove_db_file() -> None:
    """ Function to remove a database file if it exists.

    This function uses the DatabasePath class from `S3_File_Uploader.__init__.py` to determine what
    database file to remove.
    """
    # Have to create an instance variable of DatabasePath since the tests create different databases
    #   depending on the test that is running.
    # I tested by just entering `DatabasePath.get()` in the os commands bellow and the tests fail.
    db_file_path = DatabasePath.get()

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


def open_program() -> None:
    pc = ProgramController()
    return pc


def close_program(pc: ProgramController) -> None:
    pc.quit()


def destroy_program(pc: ProgramController) -> None:
    pc.destroy()
