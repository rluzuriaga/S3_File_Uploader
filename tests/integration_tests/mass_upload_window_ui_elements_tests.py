from __future__ import annotations

import os
import unittest
from typing import Any, TYPE_CHECKING

from dotenv import load_dotenv

from config import DatabasePath
from S3_File_Uploader.UI.MassUpload import MassUpload
from S3_File_Uploader.UI.SetupWindow import SetupWindow

from tests.integration_tests.utils import remove_db_file, update_program_controller_loop
from tests.integration_tests.utils import open_program, destroy_program
from tests.integration_tests.utils import ignore_aws_warning

if TYPE_CHECKING:
    from S3_File_Uploader.UI.ProgramController import ProgramController

load_dotenv()


class MassUploadWindowUIElements(unittest.TestCase):
    pc: ProgramController
    mass_upload: Any  # TODO: Figure out how to effectively annotate this

    @classmethod
    def setUpClass(cls) -> None:
        ignore_aws_warning()

        DatabasePath.path = os.path.join(os.getcwd(), 'mass_upload_window_UI_test_db.sqlite3')

        remove_db_file()

        cls.pc = open_program()

        cls._setup_app_data()

        cls.pc.add_frame_to_paned_window(MassUpload)
        update_program_controller_loop(cls.pc)

        cls.mass_upload = cls.pc.select_frame(MassUpload)

        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        destroy_program(cls.pc)

        # Need to delete the self.pc var
        # Sometimes the GUI gets stuck but somehow this helps
        del cls.pc

        remove_db_file()
        return super().tearDownClass()

    @classmethod
    def _setup_app_data(cls) -> None:
        cls.pc.add_frame_to_paned_window(SetupWindow)
        update_program_controller_loop(cls.pc)

        setup_window: Any = cls.pc.select_frame(SetupWindow)  # TODO: Figure out how to effectively annotate this

        setup_window.access_key_id_string.set(os.environ.get('AWS_ACCESS_KEY_ID'))
        setup_window.secret_key_string.set(os.environ.get('AWS_SECRET_KEY'))
        setup_window.region_name_var.set(os.environ.get('AWS_REGION_NAME'))
        setup_window.ffmpeg_input_var.set("-vcodec libx264 -crf 40")
        setup_window.save_button.invoke()

        update_program_controller_loop(cls.pc)

        cls.pc.remove_paned_window_frame(cls.pc.active_panes()[-1])

        update_program_controller_loop(cls.pc)

    def test_1_default_radio_buttons(self) -> None:
        """ Test that the all the radio buttons and checkboxes are in their default position. """
        self.assertEqual(self.mass_upload.radio_button_all.state()[0], 'selected')
        self.assertFalse(self.mass_upload.radio_button_video.state())

        self.assertFalse(
            self.mass_upload.video_checkboxes.grid_info(),
            msg='The video checkboxes are added on the grid.'
        )

    def test_2_grid_changes_from_radio_buttons(self) -> None:
        """ Test that all the grid changes take effect when clicking on the radio buttons. """
        # Click on the Videos Only radio button
        self.mass_upload.radio_button_video.invoke()
        update_program_controller_loop(self.pc)

        # Assert that the All Files radio button got unselected and the Video Only on got selected
        self.assertEqual(self.mass_upload.radio_button_video.state()[0], 'selected')
        self.assertFalse(self.mass_upload.radio_button_all.state())

        # Assert that the video checkboxes got added to grid.
        self.assertTrue(
            self.mass_upload.video_checkboxes.grid_info(),
            msg='The video checkboxes are not added on the grid.'
        )

        # Assert that the Use ffmpeg checkbox gets added to grid.
        self.assertTrue(
            self.mass_upload.use_ffmpeg_checkbox.grid_info(),
            msg='Use ffmpeg checkbox was not added to grid.'
        )

        # Click on the All Files radio button
        self.mass_upload.radio_button_all.invoke()
        update_program_controller_loop(self.pc)

        # Assert that the All Files radio button got selected and the Video Only on got unselected
        self.assertEqual(self.mass_upload.radio_button_all.state()[0], 'selected')
        self.assertFalse(self.mass_upload.radio_button_video.state())

        # Assert that the video checkboxes got removed from the grid.
        self.assertFalse(
            self.mass_upload.video_checkboxes.grid_info(),
            msg='The video checkboxes where not removed from the grid.'
        )

        # Assert that the Use ffmpeg checkbox got removed from the grid.
        self.assertFalse(
            self.mass_upload.use_ffmpeg_checkbox.grid_info(),
            msg='The Use ffmpeg checkbox was not removed from the grid.'
        )

    def test_3_video_checkboxes_invoke(self) -> None:
        """ Test that the binding text for each video checkbox is working correctly. """
        from S3_File_Uploader.Database import Database

        # Click on the Videos Only radio button
        self.mass_upload.radio_button_video.invoke()
        update_program_controller_loop(self.pc)

        # Assert that no bind text is displayed
        self.assertFalse(self.mass_upload.video_checkboxes.hover_text.cget('text'))

        # Loop through all the widgets to check if the binding is working
        for text, widget in self.mass_upload.video_checkboxes.checkbox_text_and_widgets:

            # Retrieve the text that should be displayed when binding the widget
            with Database() as DB:
                extension_text = DB.get_video_formats(False, text)

            # Trigger the <Enter> event for the widget
            widget.event_generate("<Enter>")

            # Assert that the correct text is added
            self.assertIn(", ".join(extension_text), self.mass_upload.video_checkboxes.hover_text.cget('text'))

            # Trigger the <Leave> event for the widget
            widget.event_generate("<Leave>")


if __name__ == "__main__":
    unittest.main()
