from __future__ import annotations

import os
import unittest
from typing import TYPE_CHECKING, Any

from config import DatabasePath
from S3_File_Uploader.UI.SetupWindow import SetupWindow

from tests.integration_tests.utils import remove_db_file, update_program_controller_loop
from tests.integration_tests.utils import open_program, destroy_program
from tests.integration_tests.utils import ignore_aws_warning

if TYPE_CHECKING:
    from S3_File_Uploader.UI.ProgramController import ProgramController


class SetupWindowTestUIElements(unittest.TestCase):
    pc: ProgramController
    setup_window: Any  # TODO: Figure out how to effectively annotate this

    @classmethod
    def setUpClass(cls) -> None:
        ignore_aws_warning()

        DatabasePath.path = os.path.join(os.getcwd(), 'setup_window_test_db.sqlite3')

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


if __name__ == "__main__":
    unittest.main()
