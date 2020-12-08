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
