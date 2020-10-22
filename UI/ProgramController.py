import tkinter as tk
from tkinter import ttk

from .MainWindow import MainWindow
from .SetupWindow import SetupWindow
from .MassUpload import MassUpload

class ProgramController(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Make the application not resizable
        self.resizable(False, False)
        
        self.container = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.container.pack(fill=tk.BOTH, expand=True)

        self.frames = {}

        for F in (MainWindow, SetupWindow, MassUpload):
            frame = F(self.container, self)
            self.frames[F] = frame

        # Open main page
        self.add_frame_to_paned_window(MainWindow)

        # Center the window
        screen_x, screen_y = self._get_screen_size()

        windowWidth = self.winfo_reqwidth()
        windowHeight = self.winfo_reqheight()

        # Subtract some pixels since the application opens a pane on the right
        positionRight = int((screen_x - 500)/2 - windowWidth/2)
        positionDown = int((screen_y - 200)/2 - windowHeight/2)

        self.geometry(f"+{positionRight}+{positionDown}")
    
    def _get_screen_size(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        return screen_width, screen_height
    
    def add_frame_to_paned_window(self, frame_):
        frame = self.frames[frame_]
        self.container.add(frame, weight=1)
    
    def remove_paned_window_frame(self, frame_from_active_panes):
        self.container.forget(frame_from_active_panes)
    
    def active_panes(self):
        return self.container.panes()
    
    def get_last_frame(self):
        last_frame = list(self.frames.keys())[-1]
        return last_frame
    
    def enable_main_window_buttons(self):
        mw = self.frames[MainWindow]
        mw.enable_all_buttons()
