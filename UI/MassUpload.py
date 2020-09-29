import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os

from Database import Database
from AWS import AWS

class MassUpload(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent, width=100, height=300, relief=tk.RIDGE)
        self.controller = controller

        self.open_folder_icon_path = tk.PhotoImage(file=os.getcwd() + '/UI/images/open_folder_icon.png')

        self.refresh_button_image = tk.PhotoImage(file=os.getcwd() + '/UI/images/refresh_icon.png')

        self.aws = AWS()
        self.S3_BUCKET_VALUES = self.aws.get_s3_buckets()

        self.ui_elements()
    
    def ui_elements(self):
        # Row 0
        self.header_label = ttk.Label(
            self,
            text='Start a mass upload batch',
            font=('Helvetica', 18, 'underline'),
            justify=tk.CENTER
        )
        self.header_label.grid(row=0, column=0, columnspan=2, pady=10, padx=20)

        # Row 1
        self.update_label = ttk.Label(
            self,
            text='',
            font=('Helvetica', 15),
            justify=tk.CENTER
        )
        self.update_label.grid(row=1, column=0, columnspan=2, pady=10, padx=20)

        # Row 2
        self.path_to_mass_upload_label = ttk.Label(
            self,
            text='Directory path for mass upload:',
            font=('Helvetica', 15),
            justify=tk.CENTER
        )
        self.path_to_mass_upload_label.grid(row=2, column=0 ,columnspan=2, padx=20, pady=(10, 5))

        # Row 3
        self.mass_upload_path = tk.StringVar()
        self.mass_upload_path_input_field = ttk.Entry(
            self,
            width=35,
            textvariable=self.mass_upload_path
        )
        self.mass_upload_path_input_field.grid(row=3, column=0, padx=(50, 5))

        self.mass_upload_path_label = ttk.Label(
            self,
            image=self.open_folder_icon_path
        )
        self.mass_upload_path_label.bind("<Button-1>",lambda e: self.open_folder_path())
        self.mass_upload_path_label.grid(row=3, column=1, padx=(5, 50))

        # Row 4
        self.s3_bucket_location_label = ttk.Label(
            self,
            text='Please select the S3 bucket to upload to:',
            font=('Helvetica', 15),
            justify=tk.CENTER
        )
        self.s3_bucket_location_label.grid(row=4, column=0, columnspan=2, padx=20, pady=(25, 5))
        
        # Row 5
        self.s3_bucket_name = tk.StringVar()
        self.s3_bucket_selector = ttk.Combobox(
            self,
            textvariable=self.s3_bucket_name,
            values=self.S3_BUCKET_VALUES,
            width=35,
            state='readonly'
        )
        self.s3_bucket_selector.grid(row=5, column=0, columnspan=1, padx=(50, 5))

        self.refresh_s3_buckets_label = ttk.Label(
            self,
            image=self.refresh_button_image
        )
        self.refresh_s3_buckets_label.bind("<Button-1>", lambda e: self.refresh_s3_buckets())
        self.refresh_s3_buckets_label.grid(row=5, column=1, columnspan=1, padx=(8, 50))

        # Row 6
        self.start_upload_button = ttk.Button(
            self,
            text='Start Upload',
            style='regular.TButton',
            command=self.start_upload
        )
        self.start_upload_button.grid(row=6, column=0, columnspan=2, pady=(20,15))

    def open_folder_path(self):
        path = filedialog.askdirectory()
        self.mass_upload_path.set(path)
    
    def start_upload(self):
        with Database() as DB:
            DB.add_mass_upload_data(self.mass_upload_path.get(), self.s3_bucket_name.get())

    def refresh_s3_buckets(self):
        self.update_label.configure(text='Please wait...')

        S3_BUCKET_VALUES = self.aws.get_s3_buckets()
        self.s3_bucket_selector.configure(values=S3_BUCKET_VALUES)

        self.update_label.configure(text='S3 buckets updated')
