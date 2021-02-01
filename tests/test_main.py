import os
import time
import unittest
import warnings
from shutil import which

from dotenv import load_dotenv

from S3_File_Uploader.UI.ProgramController import ProgramController
from S3_File_Uploader.UI.MainWindow import MainWindow
from S3_File_Uploader.UI.SetupWindow import SetupWindow
from S3_File_Uploader.UI.MassUpload import MassUpload

load_dotenv()


def remove_db_file():
    # Get the full path to where the database file is located.
    db_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'db.sqlite3')

    if os.path.exists(db_file_path):
        os.remove(db_file_path)


class MainTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        remove_db_file()
        warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*<ssl.SSLSocket.*>")
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        remove_db_file()
        return super().tearDownClass()

    def _update_program_controller_loop(self, seconds: int = 1) -> None:
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
                self.pc.update_idletasks()
                self.pc.update()
            else:
                break

    def test_environ_vars_available(self) -> None:
        """ Test if the environment variables a present. """
        self.assertIsNotNone(os.environ.get('AWS_ACCESS_KEY_ID'))
        self.assertIsNotNone(os.environ.get('AWS_SECRET_KEY'))
        self.assertIsNotNone(os.environ.get('AWS_REGION_NAME'))

    def test_ffmpeg_in_path(self) -> None:
        """ Test if ffmpeg is added to path. """
        self.assertIsNotNone(which('ffmpeg'))

    def test_ffprobe_in_path(self) -> None:
        """ Test if ffprobe is added to path. """
        self.assertIsNotNone(which('ffprobe'))

    def test_setup_window(self) -> None:
        """ Test that everyting in the setup window is working correctly. """

        self.pc = ProgramController()

        self.pc.add_frame_to_paned_window(SetupWindow)
        setup_window = self.pc.select_frame(SetupWindow)

        # Interact with the UI
        setup_window.access_key_id_string.set(os.environ.get('AWS_ACCESS_KEY_ID'))
        setup_window.secret_key_string.set(os.environ.get('AWS_SECRET_KEY'))
        setup_window.region_name_var.set(os.environ.get('AWS_REGION_NAME'))
        setup_window.save_button.invoke()

        self._update_program_controller_loop()

        # Make sure that the settings saved message gets displayed.
        self.assertEqual(setup_window.setup_window_output_message_variable.get(), 'Settings saved.')

        # Make sure that the save button/command actually locked the settings.
        self.assertFalse(setup_window.save_button.grid_info(), msg="Save button still on grid.")
        self.assertEqual(str(setup_window.access_key_id_input_field.cget('state')), 'disabled')
        self.assertEqual(str(setup_window.secret_key_input_field.cget('state')), 'disabled')
        self.assertEqual(str(setup_window.region_name_input_field.cget('state')), 'disabled')

        self.pc.destroy()


if __name__ == "__main__":
    unittest.main(exit=False)
