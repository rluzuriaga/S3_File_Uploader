import logging
import tkinter as tk
from tkinter import ttk

from S3_File_Uploader import APP_TITLE

from .MainWindow import MainWindow
from .SetupWindow import SetupWindow
from .MassUpload import MassUpload
from .UpdateDatabase import UpdateDatabase

# Setup logger
logger = logging.getLogger('main_logger')


class ProgramController(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        logger.debug("Initializing the Tkinter program controller.")

        # Setting App title
        self.title(APP_TITLE)

        # Make the application not resizable
        self.resizable(False, False)

        self.container = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.container.pack(fill=tk.BOTH, expand=True)

        self.frames = {}

        for F in (MainWindow, SetupWindow, UpdateDatabase, MassUpload):
            frame = F(self.container, self)
            self.frames[F] = frame

            logger.debug(f"Adding {F.__name__} to the program controller frames.")

        # Open main page
        self.add_frame_to_paned_window(MainWindow)

        # Center the window
        screen_x, screen_y = self.get_screen_size()

        windowWidth = self.winfo_reqwidth()
        windowHeight = self.winfo_reqheight()

        # Subtract some pixels since the application opens a pane on the right
        positionRight = int((screen_x - 500)/2 - windowWidth/2)
        positionDown = int((screen_y - 200)/2 - windowHeight/2)

        self.geometry(f"+{positionRight}+{positionDown}")

        logger.debug("Set location of main window on the screen.")

    def get_screen_size(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        logger.debug("Returning screen size.")

        return screen_width, screen_height

    def add_frame_to_paned_window(self, frame_):
        frame = self.frames[frame_]
        self.container.add(frame, weight=1)

        logger.debug(f'Adding "{frame_.__name__}" frame to paned window.')

    def remove_paned_window_frame(self, frame_from_active_panes):
        self.container.forget(frame_from_active_panes)
        logger.debug(f'Removing "{str(frame_from_active_panes)}" frame from paned window.')

    def active_panes(self):
        return self.container.panes()

    def get_last_frame(self):
        last_frame = list(self.frames.keys())[-1]
        return last_frame

    def enable_main_window_buttons(self):
        mw = self.frames[MainWindow]
        mw.enable_all_buttons()

        logger.debug('Enabling all "MainWindow" buttons.')

    def disable_main_window_buttons(self):
        mw = self.frames[MainWindow]
        mw.disable_all_buttons()

        logger.debug('Disabling all "MainWindow" buttons.')

    def setup_start_after(self):
        self.frames[SetupWindow].start_after()

        logger.debug('Starting the tkinter after method for "SetupWindow".')

    def setup_stop_after(self):
        self.frames[SetupWindow].stop_after()

        logger.debug('Stopping the tkinter after method for "SetupWindow".')
