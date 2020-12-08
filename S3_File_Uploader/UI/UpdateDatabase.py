import logging
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

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
            font=('Helvetica', 18, 'underline'),
            justify=tk.CENTER
        )
        top_label.grid(row=0, column=0, columnspan=2, padx=50, pady=(10, 30))

        explanation_text = 'Please select the SQL file downloaded using the button bellow.\nThen click on Update.'
        self.update_label = ttk.Label(
            self,
            text=explanation_text,
            font=('Helvetica', 15),
            justify=tk.CENTER
        )
        self.update_label.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 20))

        self.file_path = tk.StringVar()
        self.file_path_input_field = ttk.Entry(
            self,
            width=30,
            textvariable=self.file_path
        )
        self.file_path_input_field.grid(row=2, column=0, padx=(20, 10), pady=(0, 20))

        self.file_path_button = ttk.Button(
            self,
            text='Select SQL File',
            command=self._select_sql_file
        )
        self.file_path_button.grid(row=2, column=1, padx=(0, 20), pady=(0, 20))

        self.update_button = ttk.Button(
            self,
            text="Update",
            command=self._update_database
        )
        self.update_button.grid(row=3, column=0, columnspan=2, padx=30, pady=10)

    def _select_sql_file(self):
        pass

    def _update_database(self):
        pass
