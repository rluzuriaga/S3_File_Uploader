import tkinter as tk
from tkinter import ttk

from .MainWindow import MainWindow
from .SetupWindow import SetupWindow

class ProgramController(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.container = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.container.pack(fill=tk.BOTH, expand=True)

        self.frames = {}

        for F in (MainWindow, SetupWindow):
            frame = F(self.container, self)
            self.frames[F] = frame

        # Open main page
        self.add_frame_to_paned_window(MainWindow)
    
    def add_frame_to_paned_window(self, container):
        frame = self.frames[container]
        self.container.add(frame, weight=1)
    
    def remove_paned_window_frame(self, container):
        frame = self.frames[container]
        self.container.forget(frame)
    
    def active_panes(self):
        return self.container.panes()
    
    def get_last_frame(self):
        last_frame = list(self.frames.keys())[-1]
        return last_frame