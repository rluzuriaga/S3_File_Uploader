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


if __name__ == "__main__":
    unittest.main(exit=False)
