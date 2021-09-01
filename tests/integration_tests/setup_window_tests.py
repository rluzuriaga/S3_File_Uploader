import os
import unittest
from typing import Any

from dotenv import load_dotenv

from config import DatabasePath
from S3_File_Uploader.UI.SetupWindow import SetupWindow

from tests.integration_tests.utils import remove_db_file, update_program_controller_loop
from tests.integration_tests.utils import open_program, destroy_program
from tests.integration_tests.utils import ignore_aws_warning


load_dotenv()


class SetupWindowTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        ignore_aws_warning()

        DatabasePath.path = os.path.join(os.getcwd(), 'setup_window_test_db.sqlite3')

        remove_db_file()
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        remove_db_file()
        return super().tearDownClass()

    def setUp(self) -> None:
        self.pc = open_program()
        return super().setUp()

    def tearDown(self) -> None:
        destroy_program(self.pc)
        del self.pc
        return super().tearDown()

    def test_setup_window_on_fresh_database(self) -> None:
        """ Test that everyting in the setup window is working correctly. """

        self.pc.add_frame_to_paned_window(SetupWindow)
        setup_window: Any = self.pc.select_frame(SetupWindow)  # TODO: Figure out how to effectively annotate this

        update_program_controller_loop(self.pc)

        # Interact with the UI to add the AWS keys, region name, and "click" the save button
        setup_window.access_key_id_string.set(os.environ.get('AWS_ACCESS_KEY_ID'))
        setup_window.secret_key_string.set(os.environ.get('AWS_SECRET_KEY'))
        setup_window.region_name_var.set(os.environ.get('AWS_REGION_NAME'))
        setup_window.save_button.invoke()

        update_program_controller_loop(self.pc)

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


if __name__ == "__main__":
    unittest.main(exit=False)
