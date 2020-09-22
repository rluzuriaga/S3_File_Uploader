import tkinter as tk
from tkinter import ttk
import threading

from Database import Database
from AWS import *

class SetupWindow(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent, width=100, height=300, relief=tk.RIDGE)
        self.controller = controller
    
        self.ui_elements()

    def ui_elements(self):
        self.setup_window_top_label = ttk.Label(
            self,
            text='Please enter all the data.',
            font=('Helvetica', 15),
            justify=tk.CENTER
        )
        self.setup_window_top_label.grid(row=0, column=0, columnspan=2, padx=200, pady=(15, 15))

        # Label to git the user output messages like failed or success
        self.setup_window_output_message = ttk.Label(
            self,
            text='',
            font=('Helvetica', 15),
            justify=tk.CENTER
        )
        self.setup_window_output_message.grid(row=1, column=0, columnspan=2, pady=(5, 5))


        # Left labels
        self.access_key_id_label = ttk.Label(
            self,
            text='AWS Access Key ID: ',
            font=('Helvetica', 15),
            justify=tk.LEFT
        )
        self.access_key_id_label.grid(row=2, column=0, columnspan=1, padx=(0, 10), pady=(10, 0))

        self.secret_key_label = ttk.Label(
            self,
            text='AWS Secret Access Key: ',
            font=('Helvetica', 15),
            justify=tk.LEFT
        )
        self.secret_key_label.grid(row=3, column=0, columnspan=1, padx=(0, 10), pady=(10, 0))

        self.region_name_label = ttk.Label(
            self,
            text='Default Region Name: ',
            font=('Helvetica', 15),
            justify=tk.LEFT
        )
        self.region_name_label.grid(row=4, column=0, columnspan=1, padx=(0, 10), pady=(10, 0))


        # Data input fields
        self.access_key_id_string = tk.StringVar()
        self.access_key_id_input_field = ttk.Entry(
            self,
            width=44,
            textvariable=self.access_key_id_string
        )
        self.access_key_id_input_field.grid(row=2, column=1, columnspan=1, padx=(0, 10), pady=(10, 0))

        self.secret_key_string = tk.StringVar()
        self.secret_key_input_field = ttk.Entry(
            self,
            width=44,
            textvariable=self.secret_key_string
        )
        self.secret_key_input_field.grid(row=3, column=1, columnspan=1, padx=(0, 10), pady=(10, 0))

        self.region_name = tk.StringVar()
        self.region_name_input_field = ttk.Combobox(
            self,
            textvariable=self.region_name,
            # To be replaced with data from database
            values=('US East (Ohio)', 'US East (N. Virginia)', 'US West (N. California)',
                    'US West (Oregon)', 'Africa (Cape Town)', 'Asia Pacific (Hong Kong)',
                    'Asia Pacific (Mumbai)', 'Asia Pacific (Osaka-Local)', 'Asia Pacific (Seoul)',
                    'Asia Pacific (Singapore)', 'Asia Pacific (Sydney)', 'Asia Pacific (Tokyo)',
                    'Canada (Central)', 'China (Beijing)', 'China (Ningxia)',
                    'Europe (Frankfurt)', 'Europe (Ireland)', 'Europe (London)',
                    'Europe (Milan)', 'Europe (Paris)', 'Europe (Stockholm)',
                    'Middle East (Bahrain)', 'South America (São Paulo)',
                    'AWS GovCloud (US-East)', 'AWS GovCloud (US)'),
            width=42,
            state='readonly'
        )
        self.region_name_input_field.grid(row=4, column=1, columnspan=1, padx=(0, 10), pady=(10, 0))


        # Buttons
        self.save_button = ttk.Button(
            self,
            text="Save Configuration",
            style='regular.TButton',
            command=lambda: print('save')
        )
        self.save_button.grid(row=5, column=0, pady=(20, 10))

        self.lock_unlock_button = ttk.Button(
            self,
            text='Lock',
            style='regular.TButton',
            command=lambda: print('lock unlock')
        )
        self.lock_unlock_button.grid(row=5, column=1, padx=(0, 40), pady=(20, 10), sticky='E')
