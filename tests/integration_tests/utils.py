import os
import time
import _tkinter

from S3_File_Uploader import DatabasePath, LOGS_DIRECTORY
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
        # Since the tests run faster than what Python can remove the file,
        #  the function is now recursive to wait until the program actually ends
        #  before removing the database file.
        try:
            os.remove(db_file_path)
        except PermissionError:
            time.sleep(1)
            remove_db_file()


def update_program_controller_loop(program_controller: ProgramController) -> None:
    """ Run program controller updates.

    There is no need to update multiple times during a timeframe since the dooneevent function
    makes doesn't end until all the events are completed.
    The reason to include both dooneenvent() and update() is that dooneevent doesn't actually update all 
    the graphics just the events.

    Args:
        program_controller (ProgramController): The open tkinter program controller.
    """
    try:
        program_controller.dooneevent(_tkinter.ALL_EVENTS | _tkinter.DONT_WAIT)
        program_controller.update()
    except RuntimeError:
        pass


def setup_logs_for_tests() -> None:
    import logging

    log_file_path = os.path.join(LOGS_DIRECTORY, 'tests.log')

    if not os.path.exists(LOGS_DIRECTORY):
        os.makedirs(LOGS_DIRECTORY)

    logger = logging.getLogger('main_logger')
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler(log_file_path)
    fh.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(filename)s:%(funcName)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    logger.debug(f'Logger setup for tests.')


def open_program() -> None:
    """ Open the application & update the program controller loop.

    Returns:
        pc (ProgramController): The program controller for the tkinter app.
    """
    setup_logs_for_tests()

    pc = ProgramController()
    update_program_controller_loop(pc)

    return pc


def destroy_program(pc: ProgramController) -> None:
    """ Update the program controller loop then quit application. 
    Need to update the controller loop so that there are no more tkinter processes still pending.
    """
    update_program_controller_loop(pc)
    pc.quit()
    pc.destroy()
