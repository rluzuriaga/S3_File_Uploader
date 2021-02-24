import logging
import tkinter as tk
from tkinter import ttk

from config import APP_VERSION, APP_TITLE

logger = logging.getLogger('main_logger')


class UpdateApp:
    def __init__(self):
        logger.debug(f'Opening window letting the user know to download the new version of the app.')
        root = tk.Tk()
        root.title(APP_TITLE)

        main_frame = ttk.Frame(
            root, width=200, height=200, relief=tk.RIDGE)

        first_label = ttk.Label(
            main_frame,
            text=f'The software is out of date. Current version: {APP_VERSION}',
            font=('Helvetica', 15),
            justify=tk.CENTER
        )

        second_label = ttk.Label(
            main_frame,
            text='Please go to "https://github.com/rluzuriaga/S3_File_Uploader/releases" and download the latest version of the application.'
        )

        main_frame.pack(fill=tk.BOTH, expand=True)
        first_label.pack(padx=20, pady=(20, 5))
        second_label.pack(padx=20, pady=(0, 20))

        root.mainloop()
