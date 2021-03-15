from __future__ import annotations

import os
import unittest
from typing import TYPE_CHECKING

from config import DatabasePath
from S3_File_Uploader.Database import Database
from S3_File_Uploader.UI.UpdateDatabase import UpdateDatabase

from tests.integration_tests.utils import open_program, destroy_program
from tests.integration_tests.utils import remove_db_file, update_program_controller_loop
from tests.integration_tests.utils import ignore_aws_warning

if TYPE_CHECKING:
    from S3_File_Uploader.UI.ProgramController import ProgramController


class UpdateDatabaseWindowTestCase(unittest.TestCase):
    pc: ProgramController
    update_window: UpdateDatabase

    @classmethod
    def setUpClass(cls) -> None:
        ignore_aws_warning()

        DatabasePath.change_path(os.path.join(os.getcwd(), 'update_database_test_db.sqlite3'))

        remove_db_file()

        cls.pc = open_program()
        cls.pc.add_frame_to_paned_window(UpdateDatabase)
        update_program_controller_loop(cls.pc)

        # MYPY ERROR: Incompatible types in assignment (expression has type "Union[MainWindow, SetupWindow, MassUpload, UpdateDatabase]", variable has type "UpdateDatabase")
        cls.update_window = cls.pc.select_frame(UpdateDatabase)  # type: ignore
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        del cls.update_window

        destroy_program(cls.pc)
        del cls.pc

        remove_db_file()
        return super().tearDownClass()

    def test_database_update(self) -> None:
        """ Test that the Update Database functionality on the program works. """
        # Assert that the database doesn't already have the tests table
        with Database() as DB:
            self.assertIsNone(DB.get_tests_table())

        # Update the database using the database file
        sql_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'update_db.sql')

        self.update_window.file_path.set(sql_file_path)
        self.update_window.update_button.invoke()

        update_program_controller_loop(self.pc)

        # Assert that the database actually got updated with the sql file
        with Database() as DB:
            self.assertEqual(DB.get_tests_table()[0], "This is a test.")


if __name__ == "__main__":
    unittest.main(exit=False)
