from __future__ import annotations

import logging
import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING

from config import APP_VERSION, DB_VERSION
from S3_File_Uploader.Database import Database

from S3_File_Uploader.UI.SetupWindow import SetupWindow
from S3_File_Uploader.UI.UpdateDatabase import UpdateDatabase
from S3_File_Uploader.UI.MassUpload import MassUpload

if TYPE_CHECKING:
    from tkinter import ttk
    from S3_File_Uploader.UI.ProgramController import ProgramController


# Set up logger
logger = logging.getLogger('main_logger')


class MainWindow(ttk.Frame):
    def __init__(self, parent: ttk.PanedWindow, controller: ProgramController) -> None:
        ttk.Frame.__init__(self, parent, width=100, height=300, relief=tk.RIDGE)

        self.controller = controller

        logger.debug(f'Initializing the MainWindow ttk frame.')

        self.ui_elements()
        # Set the status bar labels to always be on the bottom when opening a new pane window.
        self.rowconfigure(100, weight=1)
        logger.debug(f'Created MainWindow UI elements.')

        with Database() as DB:
            if DB.are_settings_saved():
                self.enable_all_buttons()

    def ui_elements(self) -> None:
        self.main_window_top_label = ttk.Label(
            self,
            text='Please select one of the options below.',
            style='main_window_top_label.TLabel',
            justify=tk.CENTER
        )
        self.main_window_top_label.grid(row=0, column=0, columnspan=2, padx=60, pady=(10, 30))

        self.main_window_setup_button = ttk.Button(
            self,
            text="Initial Setup",
            style='regular.TButton',
            command=self.initial_setup_button_press
        )
        self.main_window_setup_button.grid(row=1, column=0, columnspan=2, pady=(0, 10))

        self.update_database_button = ttk.Button(
            self,
            text="Update Database",
            style='regular.TButton',
            command=self.update_database_button_press
        )
        self.update_database_button.grid(row=2, column=0, columnspan=2, pady=(0, 10))

        self.mass_upload_window_button = ttk.Button(
            self,
            text='Start Mass Upload',
            style='regular.TButton',
            state='disabled',
            command=self.mass_upload_button_press
        )
        self.mass_upload_window_button.grid(row=3, column=0, columnspan=2, pady=(0, 10))

        self.statusbar_app_version = ttk.Label(
            self,
            text=f'App Version: {APP_VERSION}',
            style='main_window_statusbar.TLabel'
        )
        self.statusbar_app_version.grid(row=100, column=0, padx=4, pady=(15, 2), sticky='ws')

        self.statusbar_db_version = ttk.Label(
            self,
            text=f'DB Version: {DB_VERSION}',
            style='main_window_statusbar.TLabel'
        )
        self.statusbar_db_version.grid(row=100, column=1, padx=4, pady=(15, 2), sticky='es')

    def initial_setup_button_press(self) -> None:
        """ Function that determines what happens when the 'Initial Setup' button is pressed """

        # If there is no open pane (other than the main window),
        #  then the SetupWindow pane will be added and start the after() function
        if len(self.controller.active_panes()) == 1:
            self.controller.add_frame_to_paned_window(SetupWindow)
            logger.debug(f'Attaching SetupWindow frame to window.')

            # Start the after() function to change the example ffmpeg label
            #  with what the user typed into the ffmpeg input
            self.controller.setup_start_after()

        # If the active pane is MassUpload, then the MassUpload pane is removed,
        #  the SetupWindow pane is added, and the after() function is started
        elif "massupload" in self.controller.active_panes()[-1]:
            self.controller.remove_paned_window_frame(self.controller.active_panes()[-1])
            logger.debug(f'Removing MassUpload frame from window.')

            self.controller.add_frame_to_paned_window(SetupWindow)
            logger.debug(f'Attaching SetupWindow frame to window.')

            # Start the after() function to change the example ffmpeg label
            #  with what the user typed into the ffmpeg input
            self.controller.setup_start_after()

        # If the active pane is UpdateDatabase, then the UpdateDatabase pane is removes,
        #   the SetupWindow pane will be added and start the after() function
        elif "updatedatabase" in self.controller.active_panes()[-1]:
            self.controller.remove_paned_window_frame(self.controller.active_panes()[-1])
            logger.debug(f'Removing UpdateDatabase frame from window.')

            self.controller.add_frame_to_paned_window(SetupWindow)
            logger.debug(f'Attaching SetupWindow frame to window.')

            # Start the after() function to change the example ffmpeg label
            #  with what the user typed into the ffmpeg input
            self.controller.setup_start_after()

        # If the active pane is SetupWindow, then that pane is removed
        else:
            self.controller.remove_paned_window_frame(self.controller.active_panes()[-1])
            logger.debug(f'Removing SetupWindow frame from window.')

            # Cancel the after() function so that the program doesn't eat all the CPU and RAM
            self.controller.setup_stop_after()

    def update_database_button_press(self) -> None:
        """ Function that determines what happens when the 'Update Database' button is pressed """

        # If there is no open pane (other than the main window),
        #   then the UpdateDatabase pane is added
        if len(self.controller.active_panes()) == 1:
            self.controller.add_frame_to_paned_window(UpdateDatabase)
            logger.debug(f'Attaching UpdateDatabase frame to window.')

        # If the active pane is MassUpload, then the MassUpload pane is removed,
        #   and the UpdateDatabase pane is added.
        elif "massupload" in self.controller.active_panes()[-1]:
            self.controller.remove_paned_window_frame(self.controller.active_panes()[-1])
            logger.debug(f'Removing MassUpload frame from window.')

            self.controller.add_frame_to_paned_window(UpdateDatabase)
            logger.debug(f'Attaching SetupWindow frame to window.')

        # If the active pane is SetupWindow, then the after() is stopped,
        #   the SetupWindow pane is removed, and the UpdateDatabase pane is added.
        elif "setupwindow" in self.controller.active_panes()[-1]:
            # Cancel the after() function so that the program doesn't eat all the CPU and RAM
            self.controller.setup_stop_after()

            self.controller.remove_paned_window_frame(self.controller.active_panes()[-1])
            logger.debug(f'Removing SetupWindow frame from window.')

            self.controller.add_frame_to_paned_window(UpdateDatabase)
            logger.debug(f'Attaching UpdateDatabase frame to window.')

        # If the active pane is UpdateDatabase, then that pane is removed
        else:
            self.controller.remove_paned_window_frame(self.controller.active_panes()[-1])
            logger.debug(f'Removing UpdateDatabase frame from window.')

    def mass_upload_button_press(self) -> None:
        """ Function that determines what happens when the 'Start Mass Upload' button is pressed """

        # If there is no open pane (other than the main window),
        #  then the MassUpload pane is added
        if len(self.controller.active_panes()) == 1:
            self.controller.add_frame_to_paned_window(MassUpload)
            logger.debug(f'Attaching MassUpload frame to window.')

        # If SetupWindow is the active pane, then the after() function is canceled
        #  the SetupWindow pane is removed, and the MassUpload pane is added
        elif "setupwindow" in self.controller.active_panes()[-1]:
            # Canceling the after() function from the setup window
            self.controller.setup_stop_after()

            self.controller.remove_paned_window_frame(self.controller.active_panes()[-1])
            logger.debug(f'Removing SetupWindow frame from window.')

            self.controller.add_frame_to_paned_window(MassUpload)
            logger.debug(f'Attaching MassUpload frame to window.')

        # If UpdateDatabase is the active pane, then the UpdateDatabase pane is removed,
        #   and the MassUpload pane is added
        elif "updatedatabase" in self.controller.active_panes()[-1]:
            self.controller.remove_paned_window_frame(self.controller.active_panes()[-1])
            logger.debug(f'Removing UpdateDatabase frame from window.')

            self.controller.add_frame_to_paned_window(MassUpload)
            logger.debug(f'Attaching MassUpload frame to window.')

        # If the active pane is MassUpload, then that pane is removed
        else:
            self.controller.remove_paned_window_frame(self.controller.active_panes()[-1])
            logger.debug(f'Removing MassUpload frame from window.')

    def enable_all_buttons(self) -> None:
        self.main_window_setup_button.configure(state='normal')
        self.update_database_button.configure(state='normal')
        self.mass_upload_window_button.configure(state='normal')
        logger.debug(f'Enable setup and mass upload buttons.')

    def disable_all_buttons(self) -> None:
        self.main_window_setup_button.configure(state='disabled')
        self.update_database_button.configure(state='disabled')
        self.mass_upload_window_button.configure(state='disabled')
        logger.debug(f'Disable setup and mass upload buttons.')
