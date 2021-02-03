import os
import unittest

from S3_File_Uploader import DatabasePath
from S3_File_Uploader.UI.MainWindow import MainWindow

from tests.integration_tests.utils import open_program, close_program, destroy_program
from tests.integration_tests.utils import remove_db_file, update_program_controller_loop

DatabasePath.change_path(os.path.join(os.getcwd(), 'main_window_test_db.sqlite3'))


class MainWindowTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        remove_db_file()
        cls.pc = open_program()
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        close_program(cls.pc)
        destroy_program(cls.pc)
        remove_db_file()
        return super().tearDownClass()

    def test_mass_upload_button_disabled(self) -> None:
        """ Test that the the mass upload button is actually disabled when there is no setup data in database. """
        main_window = self.pc.select_frame(MainWindow)

        # Make sure that the mass upload button is disabled before any settings are saved
        self.assertEqual(str(main_window.mass_upload_window_button.cget('state')), 'disabled')

    def test_setup_window_button(self) -> None:
        """ Test that when clicking the the Setup Window button, the SetupWindow pane gets added and removed. """
        main_window = self.pc.select_frame(MainWindow)

        # Make sure that the only active pane is mainwindow
        self.assertEqual(len(self.pc.active_panes()), 1)
        self.assertIn('mainwindow', self.pc.active_panes()[-1])

        # Click on the Setup button
        main_window.main_window_setup_button.invoke()
        update_program_controller_loop(self.pc)

        # Make sure that there are 2 active panes (MainWindow & SetupWindow)
        self.assertEqual(len(self.pc.active_panes()), 2)
        self.assertIn('setupwindow', self.pc.active_panes()[-1])


if __name__ == "__main__":
    unittest.main(exit=False)
