import logging
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from config import IS_MAC
from S3_File_Uploader.Database import Database

logger = logging.getLogger('main_logger')


class UpdateDatabase(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent, width=100, height=300, relief=tk.RIDGE)
        self.controller = controller

        logger.debug(f'Initializing the UpdateDatabase ttk frame.')

        self.ui_elements()
        logger.debug(f'Created UpdateDatabase UI elements.')

    def ui_elements(self):
        top_label = ttk.Label(
            self,
            text="Update the program's database.",
            style='update_db_top_label.TLabel',
            justify=tk.CENTER
        )
        top_label.grid(row=0, column=0, columnspan=2, padx=50, pady=(10, 30))

        explanation_text = 'Please select the SQL file downloaded using the button bellow.\nThen click on Update.'
        self.update_label = ttk.Label(
            self,
            text=explanation_text,
            style='explanation_text_label.TLabel',
            justify=tk.CENTER
        )
        self.update_label.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 20))

        self.file_path = tk.StringVar()
        self.file_path_input_field = ttk.Entry(
            self,
            width=30 if IS_MAC else 45,
            textvariable=self.file_path
        )
        self.file_path_input_field.grid(row=2, column=0, padx=(20, 10), pady=(0, 20))

        self.file_path_button = ttk.Button(
            self,
            text='Select SQL File',
            style='regular.TButton',
            command=self._select_sql_file
        )
        self.file_path_button.grid(row=2, column=1, padx=(0, 20), pady=(0, 20))

        self.update_button = ttk.Button(
            self,
            text="Update",
            style='regular.TButton',
            command=self._update_database
        )
        self.update_button.grid(row=3, column=0, columnspan=2, padx=30, pady=10)

    def _select_sql_file(self):
        """ Function that runs when the `Select SQL File` button is pressed. """

        # Open a file dialog window to select an sql file
        file_path = filedialog.askopenfile(filetypes=[('SQL files', '.sql')])
        logger.debug(f'Opening a file dialog window to select an sql file.')

        # If the user clicks on cancel, the file_path would be None.
        # The return is needed so that there is no error thrown when setting the file path
        if file_path is None:
            logger.debug(f'The user exited out of the file dialog window without selecting a file.')
            return

        logger.debug(f'User selected file: {file_path.name}')

        self.file_path.set(file_path.name)
        logger.debug(f'Setting the file path in the file path entry field.')

    def _update_database(self):
        """ Function that runs when the `Update` button is pressed. """
        # TODO: Need to find a way to validate the database update.

        logger.debug(f'Retrieving the sql file path from the file path entry box.')
        sql_file = self.file_path.get()

        with Database() as DB:
            DB.update_database_with_sql_file(sql_file)

        logger.debug(f'Database updated.')
        self.update_label.configure(text='Done!')
