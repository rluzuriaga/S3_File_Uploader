import os
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from Database import Database
from AWS import AWS
import Utils

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

    # Row 8 & 9
    VIDEO_FORMAT_GRID = {'row': 8, 'rowspan': 2, 'columnspan': 5, 'pady': 8}

    # Row 10
    START_UPLOAD_BUTTON_GRID = {'row': 10, 'column': 0, 'columnspan': 5, 'pady': (20,15)}

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent, width=100, height=300, relief=tk.RIDGE)
        self.controller = controller

        style = ttk.Style()
        style.configure('TRadiobutton', font=('Helvetica', 15))
        style.configure('TCheckbutton', font=('Helvetica', 14))

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
            command=self.all_files_radio_active
        )
        self.radio_button_all.grid(self.RADIO_BUTTON_ALL_GRID)

        self.radio_button_video = ttk.Radiobutton(
            self,
            text="Videos Only",
            value=2,
            variable=self.radio_button_var,
            command=self.video_only_radio_active
        )
        self.radio_button_video.grid(self.RADIO_BUTTON_VIDEO_GRID)

        # Row 8 & 9
        self.video_checkboxes = VideoCheckboxes(
            self,
            self.controller
        )

        # Row 10
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
        # Get the data from what the user added
        mass_upload_starting_path = self.mass_upload_path.get()
        bucket_name = self.s3_bucket_name.get()
        radio_button = self.radio_button_var.get()

        number_of_files = sum([len(files) for r, d, files in os.walk(mass_upload_starting_path)])

        with Database() as DB:
            DB.add_mass_upload_data(mass_upload_starting_path, bucket_name)

        # Create folders in bucket
        list_of_dirs = Utils.get_folders_to_create_in_bucket(mass_upload_starting_path)
        self.aws.create_multiple_folders_in_bucket(bucket_name, list_of_dirs)

        # Determine if all files to upload or just videos
        if radio_button == 1:  # All files
            # Remove the update label from the grid so that a progress bar can go instead
            self.update_label.grid_remove()
            
            self.pb = ProgressBar(self, self.controller, 400, number_of_files)
            self.pb.grid(self.UPDATE_LABEL_GRID)

            # Dictionary with the file/directory as key and Byte size as value
            #  from AWS bucket. (Used to not overwrite file that is already in the bucket)
            bucket_objects_dict = self.aws.get_bucket_objects_as_dict(bucket_name)

            # Start a new thread calling start_mass_upload_all()
            self.mass_upload_thread = threading.Thread(target=self.start_mass_upload_all, args=(mass_upload_starting_path, bucket_name, bucket_objects_dict, self.pb))
            self.mass_upload_thread.start()

        elif radio_button == 2:  # Video files
            # Get video files checkboxes
            video_checkboxes_state = self.video_checkboxes.state()
            # print([a for a in self.video_checkboxes.state()])
            pass

    def start_mass_upload_all(self, upload_start_path, bucket_name, bucket_objects_dict, progressbar):
        # Get the position of the actual folder that will get uploaded
        length_to_remove = upload_start_path.rfind('/') + 1

        for dirpath, dirnames, filenames in os.walk(upload_start_path):
            bucket_dir_path = dirpath[length_to_remove:] + '/'

            for file in filenames:
                full_path_from_pc = dirpath + '/' + file
                full_bucket_path = bucket_dir_path + file

                file_size_from_pc = os.path.getsize(full_path_from_pc)

                # If the file is already in the bucket (with the same byte size),
                #   then the loop will continue.
                if full_bucket_path in bucket_objects_dict and file_size_from_pc == bucket_objects_dict[full_bucket_path]:
                    progressbar.step()
                    continue

                with Database() as DB:
                    DB.add_file_upload(dirpath, file)

                self.aws.upload_file(full_path_from_pc, bucket_name, full_bucket_path)

                with Database() as DB:
                    DB.finish_file_upload(dirpath, file)  

                progressbar.step()

        # Finishing upload
        with Database() as DB:
            DB.finish_mass_upload()
        
        # Remove the progressbar from grid and re-add the update label
        #   letting the user know that the upload finished.
        self.pb.grid_remove()
        self.update_label.grid(self.UPDATE_LABEL_GRID)
        self.update_label.configure(text='Finished!', foreground='black')

    def refresh_s3_buckets(self):
        self.update_label.configure(text='')

        s3_bucket_values = self.aws.get_s3_buckets()
        self.s3_bucket_selector.configure(values=s3_bucket_values)

        self.update_label.configure(text='S3 buckets updated', foreground='#3fe03f') # Darker green
    
    def all_files_radio_active(self):
        if len(self.start_upload_button.grid_info()) == 0:
            self.start_upload_button.grid(self.START_UPLOAD_BUTTON_GRID)
        else:
            self.video_checkboxes.grid_forget()

    def video_only_radio_active(self):
        # Add the VideoCheckboxes frame
        self.video_checkboxes.grid(self.VIDEO_FORMAT_GRID)


class VideoCheckboxes(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent, relief=tk.FLAT)
        self.controller = controller

        self.checkbox_text = ''
        self.checkbox_variables = []

        with Database() as DB:
            self.checkbox_text = DB.get_video_formats(labels=True)

        for i, text_ in enumerate(self.checkbox_text):
            var = tk.IntVar()
            checkbox = ttk.Checkbutton(
                self,
                text=text_,
                variable=var
            )
            checkbox.grid(row=0, column=i, padx=2)
            self.checkbox_variables.append(var)

            checkbox.bind("<Enter>", self.enter_bind)
            checkbox.bind("<Leave>", self.leave_bind)

        self.hover_text = ttk.Label(
            self,
            text='',
            font=('Helvetica', 14, 'italic'),
            justify=tk.CENTER
        )
        self.hover_text.grid(row=1, column=0, columnspan=len(self.checkbox_text), pady=(3,0))

    def state(self):
        """ Returns a map of 0 or 1 for which video extension checkbox is selected. """
        return map((lambda var: var.get()), self.checkbox_variables)

    def enter_bind(self, event):
        text_ = "Includes:  "

        with Database() as DB:
            extensions = DB.get_video_formats(False, event.widget.cget('text'))

        for ext in extensions:
            text_ += ext + ", "

        self.hover_text.configure(text=text_.rstrip(', '))
    
    def leave_bind(self, event):
        self.hover_text.configure(text='')


class ProgressBar(ttk.Frame):
    def __init__(self, parent, controller, bar_size, number_of_steps):
        ttk.Frame.__init__(self, parent, relief=tk.FLAT)
        self.controller = controller

        self.number_of_steps = number_of_steps

        self.var = tk.IntVar()
        self.progressbar = ttk.Progressbar(
            self,
            orient=tk.HORIZONTAL,
            length=bar_size,
            maximum=self.number_of_steps,
            mode='determinate',
            variable=self.var
        )
        self.progressbar.pack()

    def step(self):
        # If this step is the last one to complete the progressbar
        # then change the maximum to 100 and the value to 100
        # Doing this because if it is an odd number of steps the progressbar restarts
        if self.var.get() + 1 == self.number_of_steps:
            self.progressbar.configure(maximum=100, value=100)
            return

        self.progressbar.step()
