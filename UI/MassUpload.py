import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os

from Database import Database
from AWS import AWS

class MassUpload(ttk.Frame):

    # Grids
    # Row 0
    HEADER_LABEL_GRID = {'row': 0, 'column': 0, 'columnspan': 5, 'pady': 10, 'padx': 20}

    # Row 1
    UPDATE_LABEL_GRID = {'row': 1, 'column': 0, 'columnspan': 5, 'pady': 10, 'padx': 20}

    # Row 2
    PATH_TO_MASS_UPLOAD_LABEL_GRID = {'row': 2, 'column': 0 ,'columnspan': 5, 'padx': 20, 'pady': (10, 5)}

    # Row 3
    MASS_UPLOAD_PATH_INPUT_FIELD_GRID = {'row': 3, 'column':0, 'columnspan': 4, 'padx': (50, 5), 'ipady': 4}
    MASS_UPLOAD_PATH_BUTTON_GRID = {'row': 3, 'column': 4, 'padx': (5, 50), 'ipady': 2}

    # Row 4
    S3_BUCKET_LOCATION_LABEL_GRID = {'row': 4, 'column': 0, 'columnspan': 5, 'padx': 20, 'pady': (25, 5)}

    # Row 5
    S3_BUCKET_SELECTOR_GRID = {'row': 5, 'column': 0, 'columnspan': 4, 'padx': (50, 5)}
    REFRESH_S3_BUCKETS_BUTTON_GRID = {'row': 5, 'column': 4, 'padx': (8, 50), 'ipady': 3}

    # Row 6
    RADIO_BUTTON_LABEL_GRID = {'row': 6, 'column': 0, 'columnspan': 5, 'padx': 20, 'pady': (25, 5)}

    # Row 7
    RADIO_BUTTON_ALL_GRID = {'row': 7, 'column': 0, 'padx': 1, 'sticky': 'e'}
    RADIO_BUTTON_VIDEO_GRID = {'row': 7, 'column': 1, 'padx': 1}

    # Row 8
    START_UPLOAD_BUTTON_GRID = {'row': 8, 'column': 0, 'columnspan': 2, 'pady': (20,15)}

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent, width=100, height=300, relief=tk.RIDGE)
        self.controller = controller

        style = ttk.Style()
        style.configure('TRadiobutton', font=('Helvetica', 15))

        self.aws = AWS()

        self.open_folder_icon_path = tk.PhotoImage(file=os.getcwd() + '/UI/images/open_folder_icon.png')
        self.refresh_button_image = tk.PhotoImage(file=os.getcwd() + '/UI/images/refresh_icon.png')
        
        self.S3_BUCKET_VALUES = self.aws.get_s3_buckets()

        self.ui_elements()

        self.radio_button_var.set(1)
    
    def ui_elements(self):
        # Row 0
        self.header_label = ttk.Label(
            self,
            text='Start a mass upload batch',
            font=('Helvetica', 18, 'underline'),
            justify=tk.CENTER
        )
        self.header_label.grid(self.HEADER_LABEL_GRID)

        # Row 1
        self.update_label = ttk.Label(
            self,
            text='',
            font=('Helvetica', 15),
            justify=tk.CENTER
        )
        self.update_label.grid(self.UPDATE_LABEL_GRID)

        # Row 2
        self.path_to_mass_upload_label = ttk.Label(
            self,
            text='Directory path for mass upload:',
            font=('Helvetica', 15),
            justify=tk.CENTER
        )
        self.path_to_mass_upload_label.grid(self.PATH_TO_MASS_UPLOAD_LABEL_GRID)

        # Row 3
        self.mass_upload_path = tk.StringVar()
        self.mass_upload_path_input_field = ttk.Entry(
            self,
            width=35,
            textvariable=self.mass_upload_path
        )
        self.mass_upload_path_input_field.grid(self.MASS_UPLOAD_PATH_INPUT_FIELD_GRID)

        self.mass_upload_path_button = ttk.Button(
            self,
            image=self.open_folder_icon_path,
            command=self.open_folder_path
        )
        self.mass_upload_path_button.grid(self.MASS_UPLOAD_PATH_BUTTON_GRID)

        # Row 4
        self.s3_bucket_location_label = ttk.Label(
            self,
            text='Please select the S3 bucket to upload to:',
            font=('Helvetica', 15),
            justify=tk.CENTER
        )
        self.s3_bucket_location_label.grid(self.S3_BUCKET_LOCATION_LABEL_GRID)
        
        # Row 5
        self.s3_bucket_name = tk.StringVar()
        self.s3_bucket_selector = ttk.Combobox(
            self,
            textvariable=self.s3_bucket_name,
            values=self.S3_BUCKET_VALUES,
            width=35,
            state='readonly'
        )
        self.s3_bucket_selector.grid(self.S3_BUCKET_SELECTOR_GRID)

        self.refresh_s3_buckets_button = ttk.Button(
            self,
            image=self.refresh_button_image,
            command=self.refresh_s3_buckets
        )
        self.refresh_s3_buckets_button.grid(self.REFRESH_S3_BUCKETS_BUTTON_GRID)

        # Row 6
        self.radio_button_label = ttk.Label(
            self,
            text='Please select what type file to upload:',
            font=('Helvetica', 15),
            justify=tk.CENTER
        )
        self.radio_button_label.grid(self.RADIO_BUTTON_LABEL_GRID)

        # Row 7
        self.radio_button_var = tk.IntVar()

        self.radio_button_all = ttk.Radiobutton(
            self,
            text="All Files",
            value=1,
            variable=self.radio_button_var,

            command=lambda: print(self.radio_button_var.get())
        )
        self.radio_button_all.grid(self.RADIO_BUTTON_ALL_GRID)

        self.radio_button_video = ttk.Radiobutton(
            self,
            text="Videos Only",
            value=2,
            variable=self.radio_button_var,
            command=lambda: print(self.radio_button_var.get())
        )
        self.radio_button_video.grid(self.RADIO_BUTTON_VIDEO_GRID)

        # Row 8
        self.start_upload_button = ttk.Button(
            self,
            text='Start Upload',
            style='regular.TButton',
            command=self.start_upload
        )
        self.start_upload_button.grid(self.START_UPLOAD_BUTTON_GRID)

    def open_folder_path(self):
        path = filedialog.askdirectory()
        self.mass_upload_path.set(path)
    
    def start_upload(self):
        with Database() as DB:
            DB.add_mass_upload_data(self.mass_upload_path.get(), self.s3_bucket_name.get())

    def refresh_s3_buckets(self):
        self.update_label.configure(text='')

        s3_bucket_values = self.aws.get_s3_buckets()
        self.s3_bucket_selector.configure(values=s3_bucket_values)

        self.update_label.configure(text='S3 buckets updated', foreground='#3fe03f') # Darker green
