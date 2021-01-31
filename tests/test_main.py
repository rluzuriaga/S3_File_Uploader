import os
import time
import unittest

from dotenv import load_dotenv

from S3_File_Uploader.UI.ProgramController import ProgramController
from S3_File_Uploader.UI.MainWindow import MainWindow
from S3_File_Uploader.UI.SetupWindow import SetupWindow
from S3_File_Uploader.UI.MassUpload import MassUpload

load_dotenv()


def remove_db_file():
    # TODO: Figure out if this is searching in the right directory every time.
    #       It for sure is wrong if running the file inside of the tests direcotry.
    if os.path.exists(os.path.join(os.getcwd(), 'db.sqlite3')):
        os.remove(os.path.join(os.getcwd(), 'db.sqlite3'))


class MainTestCase(unittest.TestCase):
    pc = ProgramController()

    def _update_program_controller_loop(self, seconds: int) -> None:
        """ Run a loop for the guiven seconds that updates idle tasks and user input tasks.
        This function needs to be used because to be able to test Tkinter UI elements , the test
        cannot use the mainloop function of tkinter. That means that Tkinter needs to be updated manually.

        Args:
            seconds (int): Seconds to run the loop.
                Each second, the update and update_idletasks functions run around 2600 times (depending on CPU clock speed).
        """

        secs = seconds
        start_time = time.time()
        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time

            if elapsed_time < secs:
                self.pc.update_idletasks()
                self.pc.update()
            else:
                break

    def test_aws_configuration(self):
        """ Test that there was a successful message given after saving AWS configuration. """

        self.pc.add_frame_to_paned_window(SetupWindow)
        setup_window = self.pc.select_frame(SetupWindow)

        setup_window.access_key_id_string.set(os.environ.get('AWS_ACCESS_KEY_ID'))
        setup_window.secret_key_string.set(os.environ.get('AWS_SECRET_KEY'))
        setup_window.region_name_var.set(os.environ.get('AWS_REGION_NAME'))
        setup_window.save_button.invoke()

        self._update_program_controller_loop(1)

        self.assertEqual(setup_window.setup_window_output_message_variable.get(), 'Settings saved.')

        self.pc.destroy()


if __name__ == "__main__":
    remove_db_file()

    unittest.main(exit=False)
