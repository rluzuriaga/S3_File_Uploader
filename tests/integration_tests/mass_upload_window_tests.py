import os
import unittest
import threading

from S3_File_Uploader import DatabasePath
from S3_File_Uploader.AWS import AWS
from S3_File_Uploader.UI.MassUpload import MassUpload
from S3_File_Uploader.UI.SetupWindow import SetupWindow

from tests.integration_tests.utils import remove_db_file, update_program_controller_loop
from tests.integration_tests.utils import open_program, destroy_program


DATA_DIRECTORY_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')


class MassUploadWindowTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        DatabasePath.change_path(os.path.join(os.getcwd(), 'mass_upload_window_test_db.sqlite3'))

        remove_db_file()

        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        # Need to remove the tests data before removing the DB file
        AWS().remove_tests_data(os.environ.get('S3_BUCKET'))

        remove_db_file()

        return super().tearDownClass()

    def setUp(self) -> None:
        self.pc = open_program()
        return super().setUp()

    def tearDown(self) -> None:
        destroy_program(self.pc)

        # Need to delete the self.pc var
        # Sometimes the GUI gets stuck but somehow this helps
        del self.pc
        return super().tearDown()

    def _setup_app_data(self) -> None:
        self.pc.add_frame_to_paned_window(SetupWindow)
        update_program_controller_loop(self.pc)

        setup_window = self.pc.select_frame(SetupWindow)

        setup_window.access_key_id_string.set(os.environ.get('AWS_ACCESS_KEY_ID'))
        setup_window.secret_key_string.set(os.environ.get('AWS_SECRET_KEY'))
        setup_window.region_name_var.set(os.environ.get('AWS_REGION_NAME'))
        setup_window.ffmpeg_input_var.set("-vcodec libx264 -crf 40")
        setup_window.save_button.invoke()

        update_program_controller_loop(self.pc)

        self.pc.remove_paned_window_frame(self.pc.active_panes()[-1])

        update_program_controller_loop(self.pc)

    def _upload_all_files(self) -> None:
        self.pc.add_frame_to_paned_window(MassUpload)
        update_program_controller_loop(self.pc)

        mass_upload = self.pc.select_frame(MassUpload)

        # Add data directory path to mass upload path entry box
        mass_upload.mass_upload_path.set(DATA_DIRECTORY_PATH)

        # Set bucket to use from env var
        mass_upload.s3_bucket_name.set(os.environ.get('S3_BUCKET'))

        # Click on the start upload button
        mass_upload.start_upload_button.invoke()

        # Have to run a new thread that would kill the mainloop after 3 seconds. If internet is slow make the number larger.
        # This needs to be done because once the mainloop gets called it won't stop unless it is done
        #   this way or manually.
        threading.Thread(target=self.pc.after, args=(3000, self.pc.quit)).start()

        # Run the mainloop so that the upload will execute on the same thread as the mainloop
        # If the mainloop is not called, then an exception will be raised `RuntimeError: main thread is not in main loop`
        self.pc.mainloop()

    def test_1_refresh_aws_s3_buckets(self) -> None:
        """ Test that the S3 bucket update button works correctly. """
        self._setup_app_data()

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

    def test_2_all_file_upload(self) -> None:
        """ Test that the all files method of uploading data is working.
        This test uses the `data` directory to upload to the S3 bucket in the environment var.
        """
        self._upload_all_files()

        mass_upload = self.pc.select_frame(MassUpload)

        # Assert that the finished label gets added
        self.assertEqual(mass_upload.update_label.cget('text'), 'Finished!')

        # Get all the files with their file size (bytes) from AWS
        all_files_in_s3_dict = AWS().get_bucket_objects_as_dict(os.environ.get('S3_BUCKET'))

        # Get all the local file names from the data folder
        all_local_files = []
        for a, b, filenames in os.walk(DATA_DIRECTORY_PATH):
            all_local_files = filenames

        # Assert that the file name and size are the same from local to AWS
        for s3_file, s3_file_size in all_files_in_s3_dict.items():
            # Get just the filename without the `data/` prefix
            s3_file = s3_file.split('/', 1)[1]

            local_file_size = os.path.getsize(os.path.join(DATA_DIRECTORY_PATH, s3_file))

            self.assertIn(s3_file, all_local_files)
            self.assertEqual(local_file_size, s3_file_size)

    def test_3_file_skip_already_in_s3(self) -> None:
        """ Test that the files don't get uploaded again since they are already in S3. 
        The function first retrieves the object data from the bucket after the upload from the previous test.
        Then tries to upload the same files again, which should not actually upload since the files are already in the bucket.
        Finally, it retrieves the object data from the bucket again and assert that the pre and post data are the same.

        If the test fails, it is because there was a file that changes and actually got uploaded to S3.
        """
        aws_file_data_pre_upload = AWS().get_all_objects_from_bucket(os.environ.get('S3_BUCKET'))['Contents']

        self._upload_all_files()

        aws_file_data_post_upload = AWS().get_all_objects_from_bucket(os.environ.get('S3_BUCKET'))['Contents']

        self.assertEqual(aws_file_data_pre_upload, aws_file_data_post_upload)

    # TODO: Add test for ffmpeg file upload


if __name__ == "__main__":
    unittest.main(exit=False)
