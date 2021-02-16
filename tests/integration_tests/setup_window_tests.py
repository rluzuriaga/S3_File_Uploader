import os
import unittest
import warnings

from dotenv import load_dotenv

from S3_File_Uploader import DatabasePath
from S3_File_Uploader.UI.SetupWindow import SetupWindow

from tests.integration_tests.utils import remove_db_file, update_program_controller_loop
from tests.integration_tests.utils import open_program, destroy_program


load_dotenv()

# Ignoring boto3 warning.
#   There is an open issue for boto3 about this error but is not fixed yet so I am forced to ignore the warning.
#   More info: https://github.com/boto/boto3/issues/454
warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed*")


class SetupWindowTestUIElements(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        DatabasePath.change_path(os.path.join(os.getcwd(), 'setup_window_test_db.sqlite3'))

        remove_db_file()

        cls.pc = open_program()
        cls.pc.add_frame_to_paned_window(SetupWindow)
        update_program_controller_loop(cls.pc)

        cls.setup_window = cls.pc.select_frame(SetupWindow)

        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        del cls.setup_window

        destroy_program(cls.pc)
        del cls.pc

        remove_db_file()
        return super().tearDownClass()

    def test_1_different_output_extension_for_aws_checkbox(self) -> None:
        """ Test that the different output extension for AWS entry box gets added to the grid when clicking the checkbox. """
        # "Click" on the `Different output extension for AWS` checkbox
        self.setup_window.different_ffmpeg_output_extension_checkbutton.invoke()
        update_program_controller_loop(self.pc)

        # Make sure that the different output extension entry box gets added to the grid
        self.assertTrue(
            self.setup_window.different_ffmpeg_output_extension_input.grid_info(),
            msg='The different output extension for AWS was not added to the grid.'
        )

    def test_2_save_locally_checkbox(self) -> None:
        """ Test that the local save entry box and button get added to the grid when clicking the checkbox. """
        # "Click" on the `Save locally` checkbox
        self.setup_window.local_save_checkbox.invoke()
        update_program_controller_loop(self.pc)

        # Make sure that the save locally entry box and button get added to the grid
        self.assertTrue(
            self.setup_window.local_save_path_input_field.grid_info(),
            msg='The local save path input field was not added to the grid.'
        )
        self.assertTrue(
            self.setup_window.local_save_path_button.grid_info(),
            msg='The local save path button was not added to the grid.'
        )

    def test_3_different_local_output_extension_checkbox(self) -> None:
        """ Test that the local save output extension entry box gets added to the grid when clicking the checkbox. """
        # "Click" on the `Different local output extension` checkbox
        self.setup_window.local_save_different_extension_checkbox.invoke()
        update_program_controller_loop(self.pc)

        # Make sure that the save locally entry box and button get added to the grid
        self.assertTrue(
            self.setup_window.local_save_different_output_extension_input.grid_info(),
            msg='The local different output extension input field was not added to the grid.'
        )


class SetupWindowTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        DatabasePath.change_path(os.path.join(os.getcwd(), 'setup_window_test_db.sqlite3'))

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
        setup_window = self.pc.select_frame(SetupWindow)

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
