import os
import time
import unittest
import warnings
from pathlib import Path

from dotenv import load_dotenv

from .utils import remove_db_file, update_program_controller_loop

from S3_File_Uploader.UI.ProgramController import ProgramController
from S3_File_Uploader.UI.MainWindow import MainWindow
from S3_File_Uploader.UI.SetupWindow import SetupWindow
from S3_File_Uploader.UI.MassUpload import MassUpload

load_dotenv()


class SetupWindowTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        remove_db_file()
        warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*<ssl.SSLSocket.*>")
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        remove_db_file()
        return super().tearDownClass()

    def test_setup_window_on_fresh_database(self) -> None:
        """ Test that everyting in the setup window is working correctly. """

        self.pc = ProgramController()

        self.pc.add_frame_to_paned_window(SetupWindow)
        main_window = self.pc.select_frame(MainWindow)
        setup_window = self.pc.select_frame(SetupWindow)

        # Make sure that the mass upload button is disabled before any settings are saved
        self.assertEqual(str(main_window.mass_upload_window_button.cget('state')), 'disabled')

        # Interact with the UI to add the AWS keys, region name, and "click" the save button
        setup_window.access_key_id_string.set(os.environ.get('AWS_ACCESS_KEY_ID'))
        setup_window.secret_key_string.set(os.environ.get('AWS_SECRET_KEY'))
        setup_window.region_name_var.set(os.environ.get('AWS_REGION_NAME'))
        setup_window.save_button.invoke()

        update_program_controller_loop(self.pc)

        # Make sure that the mass upload button is now enabled after the save
        self.assertEqual(str(main_window.mass_upload_window_button.cget('state')), 'normal')

        # Make sure that the settings saved message gets displayed.
        self.assertEqual(setup_window.setup_window_output_message_variable.get(), 'Settings saved.')

        # Make sure that the save button/command actually locked the settings.
        self.assertFalse(setup_window.save_button.grid_info(), msg="Save button still on grid.")
        self.assertEqual(str(setup_window.access_key_id_input_field.cget('state')), 'disabled')
        self.assertEqual(str(setup_window.secret_key_input_field.cget('state')), 'disabled')
        self.assertEqual(str(setup_window.region_name_input_field.cget('state')), 'disabled')

        # Interact with the UI to unlock the settings
        setup_window.lock_unlock_button.invoke()
        update_program_controller_loop(self.pc)

        # Make sure that the unlock button actually unlocks the settings
        self.assertTrue(setup_window.save_button.grid_info(), msg="Save button not on grid.")
        self.assertEqual(str(setup_window.access_key_id_input_field.cget('state')), 'normal')
        self.assertEqual(str(setup_window.secret_key_input_field.cget('state')), 'normal')
        self.assertEqual(str(setup_window.region_name_input_field.cget('state')), 'readonly')

        self.pc.destroy()


if __name__ == "__main__":
    unittest.main(exit=False)
