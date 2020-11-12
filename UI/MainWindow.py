import tkinter as tk
from tkinter import ttk

from Database import Database

from .SetupWindow import SetupWindow
from .MassUpload import MassUpload


class MainWindow(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent, width=100,
                           height=300, relief=tk.RIDGE)
        self.controller = controller

        self.ui_elements()

        with Database() as DB:
            if DB.are_settings_saved():
                self.enable_all_buttons()

    def ui_elements(self):
        self.main_window_top_label = ttk.Label(
            self,
            text='Please select one of the options below.',
            font=('Helvetica', 15),
            justify=tk.CENTER
        )
        self.main_window_top_label.grid(
            row=0, column=0, padx=60, pady=(10, 30))

        self.main_window_setup_button = ttk.Button(
            self,
            text="Initial Setup",
            style='regular.TButton',
            command=self.initial_setup_button_press
        )
        self.main_window_setup_button.grid(row=1, column=0, pady=(0, 10))

        self.mass_upload_window_button = ttk.Button(
            self,
            text='Start Mass Upload',
            style='regular.TButton',
            state='disabled',
            command=self.mass_upload_button_press
        )
        self.mass_upload_window_button.grid(row=2, column=0, pady=(0, 10))

    def initial_setup_button_press(self):
        """ Function that determines what happens when the 'Initial Setup' button is pressed """

        # If there is no open pane (other than the main window),
        #  then the SetupWindow pane will be added and start the after() function
        if len(self.controller.active_panes()) == 1:
            self.controller.add_frame_to_paned_window(SetupWindow)

            # Start the after() function to change the example ffmpeg label
            #  with what the user typed into the ffmpeg input
            self.controller.setup_start_after()

        # If the active pane is MassUpload, then the MassUpload pane is removed,
        #  the SetupWindow pane is added, and the after() function is started
        elif "massupload" in self.controller.active_panes()[-1]:
            self.controller.remove_paned_window_frame(
                self.controller.active_panes()[-1])
            self.controller.add_frame_to_paned_window(SetupWindow)

            # Start the after() function to change the example ffmpeg label
            #  with what the user typed into the ffmpeg input
            self.controller.setup_start_after()

        # If the active pane is SetupWindow, then that pane is removed
        else:
            self.controller.remove_paned_window_frame(
                self.controller.active_panes()[-1])

            # Cancel the after() function so that the program doesn't eat all the CPU and RAM
            self.controller.setup_stop_after()

    def mass_upload_button_press(self):
        """ Function that determines what happens when the 'Start Mass Upload' button is pressed """

        # If there is no open pane (other than the main window),
        #  then the MassUpload pane is added
        if len(self.controller.active_panes()) == 1:
            self.controller.add_frame_to_paned_window(MassUpload)

        # If SetupWindow is the active pane, then the after() function is canceled
        #  the SetupWindow pane is removed, and the MassUpload pane is added
        elif "setupwindow" in self.controller.active_panes()[-1]:
            # Canceling the after() function from the setup window
            self.controller.setup_stop_after()

            self.controller.remove_paned_window_frame(
                self.controller.active_panes()[-1])
            self.controller.add_frame_to_paned_window(MassUpload)

        # If the active pane is MassUpload, then that pane is removed
        else:
            self.controller.remove_paned_window_frame(
                self.controller.active_panes()[-1])

    def enable_all_buttons(self):
        self.main_window_setup_button.configure(state='normal')
        self.mass_upload_window_button.configure(state='normal')

    def disable_all_buttons(self):
        self.main_window_setup_button.configure(state='disabled')
        self.mass_upload_window_button.configure(state='disabled')
