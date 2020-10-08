import tkinter as tk
from tkinter import ttk

from Database import Database

from .SetupWindow import SetupWindow
from .MassUpload import MassUpload

class MainWindow(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent, width=100, height=300, relief=tk.RIDGE)
        self.controller = controller

        self.ui_elements()

        with Database() as DB:
            if DB.is_aws_config_saved():
                self.enable_all_buttons()

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

        self.mass_upload_window_button = ttk.Button(
            self,
            text='Start Mass Upload',
            style='regular.TButton',
            state='disabled',
            command=self.mass_upload_button_press
        )
        self.mass_upload_window_button.grid(row=2, column=0, pady=(0,10))

    def initial_setup_button_press(self):
        if len(self.controller.active_panes()) == 1:
            self.controller.add_frame_to_paned_window(SetupWindow)
        elif "massupload" in self.controller.active_panes()[-1]:
            self.controller.remove_paned_window_frame(self.controller.active_panes()[-1])
            self.controller.add_frame_to_paned_window(SetupWindow)
        else:
            self.controller.remove_paned_window_frame(self.controller.active_panes()[-1])

    def mass_upload_button_press(self):
        if len(self.controller.active_panes()) == 1:
            self.controller.add_frame_to_paned_window(MassUpload)
        elif "setupwindow" in self.controller.active_panes()[-1]:
            self.controller.remove_paned_window_frame(self.controller.active_panes()[-1])
            self.controller.add_frame_to_paned_window(MassUpload)
        else:
            self.controller.remove_paned_window_frame(self.controller.active_panes()[-1])
    
    def enable_all_buttons(self):
        self.mass_upload_window_button.configure(state='normal')
