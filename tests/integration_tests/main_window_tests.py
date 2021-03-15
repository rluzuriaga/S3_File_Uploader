import os
import unittest
from typing import Any

from config import DatabasePath
from S3_File_Uploader.UI.MainWindow import MainWindow

from tests.integration_tests.utils import open_program, destroy_program
from tests.integration_tests.utils import remove_db_file, update_program_controller_loop


class MainWindowTestCase(unittest.TestCase):
    main_window: Any  # TODO: Figure out how to effectively annotate this

    @classmethod
    def setUpClass(cls) -> None:
        DatabasePath.change_path(os.path.join(os.getcwd(), 'main_window_test_db.sqlite3'))

        remove_db_file()
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        remove_db_file()
        return super().tearDownClass()

    def setUp(self) -> None:
        self.pc = open_program()
        self.main_window = self.pc.select_frame(MainWindow)
        return super().setUp()

    def tearDown(self) -> None:
        destroy_program(self.pc)
        del self.pc
        return super().tearDown()

    def test_mass_upload_button_disabled(self) -> None:
        """ Test that the the mass upload button is actually disabled when there is no setup data in database. """
        # Make sure that the mass upload button is disabled before any settings are saved
        self.assertEqual(str(self.main_window.mass_upload_window_button.cget('state')), 'disabled')

    def test_one_pane_when_opening_window(self) -> None:
        """ Test that there is only one active pane when opening the application. """
        # Make sure that the only active pane is mainwindow
        self.assertEqual(len(self.pc.active_panes()), 1)
        self.assertIn('mainwindow', self.pc.active_panes()[-1])

    def test_setup_window_button(self) -> None:
        """ Test that when clicking the the Setup Window button, the SetupWindow pane gets added and removed after clicking it again. """
        # Click on the Setup button. This should add the SetupWindow pane.
        self.main_window.main_window_setup_button.invoke()
        update_program_controller_loop(self.pc)

        # Make sure that there are 2 active panes (MainWindow & SetupWindow).
        self.assertEqual(len(self.pc.active_panes()), 2)
        self.assertIn('setupwindow', self.pc.active_panes()[-1])

        # Click on the Setup button again. This should make it that the MainWindow is the only active pane.
        self.main_window.main_window_setup_button.invoke()
        update_program_controller_loop(self.pc)

        # Make sure that the SetupWindow pane actually gets closed.
        self.assertEqual(len(self.pc.active_panes()), 1)
        self.assertIn('mainwindow', self.pc.active_panes()[-1])

    def test_update_database_window_button(self) -> None:
        """ Test that when clicking the the Update Database button, the UpdateDatabase pane gets added and removed after clicking it again. """
        # Click on the Update Database button. This should add the UpdateDatabase pane.
        self.main_window.update_database_button.invoke()
        update_program_controller_loop(self.pc)

        # Make sure that there are 2 active panes (MainWindow & UpdateDatabase).
        self.assertEqual(len(self.pc.active_panes()), 2)
        self.assertIn('updatedatabase', self.pc.active_panes()[-1])

        # Click on the Update Database button again. This should make it that the MainWindow is the only active pane.
        self.main_window.update_database_button.invoke()
        update_program_controller_loop(self.pc)

        # Make sure that the UpdateDatabase pane actually gets closed.
        self.assertEqual(len(self.pc.active_panes()), 1)
        self.assertIn('mainwindow', self.pc.active_panes()[-1])

    def test_mass_upload_window_button(self) -> None:
        """ Test that when clicking the the Start Mass Upload button, the MassUpload pane gets added and removed after clicking it again. """
        # Enable the Start Mass Upload button since there is no configuration saved in the DB.
        self.main_window.mass_upload_window_button.configure(state='normal')

        # Click on the Start Mass Upload button. This should add the MassUpload pane.
        self.main_window.mass_upload_window_button.invoke()
        update_program_controller_loop(self.pc)

        # Make sure that there are 2 active panes (MainWindow & MassUpload).
        self.assertEqual(len(self.pc.active_panes()), 2)
        self.assertIn('massupload', self.pc.active_panes()[-1])

        # Click on the Start Mass Upload button again. This should make it that the MainWindow is the only active pane.
        self.main_window.mass_upload_window_button.invoke()
        update_program_controller_loop(self.pc)

        # Make sure that the MassUpload pane actually gets closed.
        self.assertEqual(len(self.pc.active_panes()), 1)
        self.assertIn('mainwindow', self.pc.active_panes()[-1])

    def test_mixing_buttons(self) -> None:
        """ Test that when clicking any button the correct pane gets added after removing the pane that was currently open.

        This test differs from the ones above because it isn't clicking the same button to close the pane.
        Instead, it is clicking another window button.
            This makes the previous window pane get removed and add the pane from the button clicked.
        """
        # Enable the Start Mass Upload button since there is no configuration saved in the DB.
        self.main_window.mass_upload_window_button.configure(state='normal')

        # Click the Setup button.
        self.main_window.main_window_setup_button.invoke()
        update_program_controller_loop(self.pc)

        # Make sure that the SetupWindow pane is active
        self.assertIn('setupwindow', self.pc.active_panes()[-1])

        # Click the Update Database button.
        self.main_window.update_database_button.invoke()
        update_program_controller_loop(self.pc)

        # Make sure that the UpdateDatabase pane is active
        self.assertIn('updatedatabase', self.pc.active_panes()[-1])

        # Click the Mass Upload button
        self.main_window.mass_upload_window_button.invoke()
        update_program_controller_loop(self.pc)

        # Make sure that the MassUpload pane is active
        self.assertIn('massupload', self.pc.active_panes()[-1])


if __name__ == "__main__":
    unittest.main(exit=False)
