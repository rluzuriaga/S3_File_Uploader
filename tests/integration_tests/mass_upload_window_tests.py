import os
import unittest

from S3_File_Uploader import DatabasePath
from S3_File_Uploader.UI.MassUpload import MassUpload
from S3_File_Uploader.UI.SetupWindow import SetupWindow

from tests.integration_tests.utils import remove_db_file, update_program_controller_loop
from tests.integration_tests.utils import open_program, destroy_program


class MassUploadWindowTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        DatabasePath.change_path(os.path.join(os.getcwd(), 'mass_upload_window_test_db.sqlite3'))

        remove_db_file()

        cls.pc = open_program()
        cls._setup_app_data()

        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        destroy_program(cls.pc)
        remove_db_file()
        return super().tearDownClass()

    @classmethod
    def _setup_app_data(cls) -> None:
        cls.pc.add_frame_to_paned_window(SetupWindow)
        update_program_controller_loop(cls.pc)

        setup_window = cls.pc.select_frame(SetupWindow)

        setup_window.access_key_id_string.set(os.environ.get('AWS_ACCESS_KEY_ID'))
        setup_window.secret_key_string.set(os.environ.get('AWS_SECRET_KEY'))
        setup_window.region_name_var.set(os.environ.get('AWS_REGION_NAME'))
        setup_window.ffmpeg_input_var.set("-vcodec libx264 -crf 40")
        setup_window.save_button.invoke()

        update_program_controller_loop(cls.pc)

        cls.pc.remove_paned_window_frame(cls.pc.active_panes()[-1])

        update_program_controller_loop(cls.pc)

    def test_1_refresh_aws_s3_buckets(self) -> None:
        """ Test that the S3 bucket update button works correctly. """
        self.pc.add_frame_to_paned_window(MassUpload)
        update_program_controller_loop(self.pc)

        mass_upload = self.pc.select_frame(MassUpload)

        # Assert that there is no data for S3 buckets
        self.assertFalse(mass_upload.s3_bucket_selector.cget('values'))

        # Click on refresh aws s3 bucket button
        mass_upload.refresh_s3_buckets_button.invoke()
        update_program_controller_loop(self.pc)

        # Assert that the updated label gets added
        self.assertEqual(mass_upload.update_label.cget('text'), 'S3 buckets updated')

        # Assert that the buckets get updated
        self.assertTrue(mass_upload.s3_bucket_selector.cget('values'))


if __name__ == "__main__":
    unittest.main(exit=False)
