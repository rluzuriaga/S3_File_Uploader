import tkinter as tk
from tkinter import ttk

from Database import Database

from .MainWindow import MainWindow
from .SetupWindow import SetupWindow
from .MassUpload import MassUpload

class ProgramController(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.container = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.container.pack(fill=tk.BOTH, expand=True)

        self.frames = {}

        for F in (MainWindow, SetupWindow, MassUpload):
            frame = F(self.container, self)
            self.frames[F] = frame

        # Open main page
        self.add_frame_to_paned_window(MainWindow)
    
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
