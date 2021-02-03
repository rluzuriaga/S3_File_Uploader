import unittest

from S3_File_Uploader.UI.MainWindow import MainWindow

from tests.integration_tests.utils import remove_db_file, open_program, close_program


class MainWindowTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        remove_db_file()
        cls.pc = open_program()
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        close_program(cls.pc)
        return super().tearDownClass()

    def test_mass_upload_button_disabled(self) -> None:
        """ Test that the the mass upload button is actually disabled when there is no setup data in database. """
        main_window = self.pc.select_frame(MainWindow)

        # Make sure that the mass upload button is disabled before any settings are saved
        self.assertEqual(str(main_window.mass_upload_window_button.cget('state')), 'disabled')


if __name__ == "__main__":
    unittest.main(exit=False)
