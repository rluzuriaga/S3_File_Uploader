from __future__ import annotations

import os
import time
import warnings

from config import DatabasePath, LOGS_DIRECTORY, IS_WINDOWS
from S3_File_Uploader.UI.ProgramController import ProgramController


def remove_db_file() -> None:
    """ Function to remove a database file if it exists.

    This function uses the DatabasePath class from `S3_File_Uploader.__init__.py` to determine what
    database file to remove.
    """
    if os.path.exists(DatabasePath.path):
        # Since the tests run faster than what Python can remove the file,
        #  the function is now recursive to wait until the program actually ends
        #  before removing the database file.
        try:
            os.remove(DatabasePath.path)
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
        # The dooneevent command doesn't work on Mac.
        # Returning error: `Tcl_WaitForEvent: Notifier not initialized`
        if IS_WINDOWS:
            import _tkinter
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


def open_program() -> ProgramController:
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


def ignore_aws_warning() -> None:
    # Ignoring boto3 warning.
    #   There is an open issue for boto3 about this error but is not fixed yet so I am forced to ignore the warning.
    #   More info: https://github.com/boto/boto3/issues/454
    warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*")
