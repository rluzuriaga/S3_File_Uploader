import tkinter as tk
from tkinter import ttk

from .SetupWindow import SetupWindow

class MainWindow(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent, width=100, height=300, relief=tk.RIDGE)
        self.controller = controller

        self.ui_elements()

    def ui_elements(self):
        self.main_window_top_label = ttk.Label(
            self, 
            text='Please select one of the options below.', 
            font=('Helvetica', 15), 
            justify=tk.CENTER
        )
        self.main_window_top_label.grid(row=0, column=0, padx=60, pady=(10, 30))

        self.main_window_setup_button = ttk.Button(
            self,
            text="Initial Setup",
            style='regular.TButton',
            command=self.initial_setup_button_press
        )
        self.main_window_setup_button.grid(row=1, column=0, pady=(0,10))

    def initial_setup_button_press(self):
        if len(self.controller.active_panes()) == 1:
            self.controller.add_frame_to_paned_window(SetupWindow)
        else:
            self.controller.remove_paned_window_frame(self.controller.get_last_frame())
