import os
import logging
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from typing import List

import pexpect
import ffmpeg

from Database import Database
from AWS import AWS


logger = logging.getLogger('main_logger')


class MassUpload(ttk.Frame):
    # Grids
    # Row 0
    HEADER_LABEL_GRID = {'row': 0, 'column': 0, 'columnspan': 5, 'pady': 10, 'padx': 20}

    # Row 1
    UPDATE_LABEL_GRID = {'row': 1, 'column': 0, 'columnspan': 5, 'pady': 10, 'padx': 20}

    # Progressbar takes over the update label grid and pushes everything else down
    OVERALL_PROGRESSBAL_LABEL_GRID = {'row': 1, 'column': 0, 'columnspan': 5, 'pady': (10, 0), 'padx': 20}

    # Row 2
    OVERALL_PROGRESSBAR_GRID = {'row': 2, 'column': 0, 'columnspan': 5, 'pady': (0, 10), 'padx': 20}

    # Row 3
    FFMPEG_AND_UPLOAD_PROGRESSBAR_LABEL_GRID = {'row': 3, 'column': 0, 'columnspan': 5, 'pady': (10, 0), 'padx': 20}

    # Row 4
    FFMPEG_AND_UPLOAD_PROGRESSBAR_GRID = {'row': 4, 'column': 0, 'columnspan': 5, 'pady': (0, 10), 'padx': 20}

    # Row 5
    PATH_TO_MASS_UPLOAD_LABEL_GRID = {'row': 5, 'column': 0, 'columnspan': 5, 'padx': 20, 'pady': (10, 5)}

    # Row 6
    MASS_UPLOAD_PATH_INPUT_FIELD_GRID = {'row': 6, 'column': 0, 'columnspan': 4, 'padx': (50, 5), 'ipady': 4}
    MASS_UPLOAD_PATH_BUTTON_GRID = {'row': 6, 'column': 4, 'padx': (5, 50), 'ipady': 2}

    # Row 7
    S3_BUCKET_LOCATION_LABEL_GRID = {'row': 7, 'column': 0, 'columnspan': 5, 'padx': 20, 'pady': (25, 5)}

    # Row 8
    S3_BUCKET_SELECTOR_GRID = {'row': 8, 'column': 0, 'columnspan': 4, 'padx': (50, 5)}
    REFRESH_S3_BUCKETS_BUTTON_GRID = {'row': 8, 'column': 4, 'padx': (8, 50), 'ipady': 3}

    # Row 9
    RADIO_BUTTON_LABEL_GRID = {'row': 9, 'column': 0, 'columnspan': 5, 'padx': 20, 'pady': (25, 5)}

    # Row 10
    RADIO_BUTTON_ALL_GRID = {'row': 10, 'column': 0, 'padx': 1, 'sticky': 'e'}
    RADIO_BUTTON_VIDEO_GRID = {'row': 10, 'column': 1, 'padx': 1}
    RADIO_BUTTON_AUDIO_GRID = {'row': 10, 'column': 2, 'padx': 1}

    # Row 11 & 12
    VIDEO_FORMAT_GRID = {'row': 11, 'rowspan': 2, 'columnspan': 5, 'pady': 8}

    # Row 13
    USE_FFMPEG_GRID = {'row': 13, 'column': 0, 'columnspan': 5, 'padx': 20}

    # Row 14
    START_UPLOAD_BUTTON_GRID = {'row': 14, 'column': 0, 'columnspan': 5, 'pady': (20, 15)}

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent, width=100,
                           height=300, relief=tk.RIDGE)
        self.controller = controller

        logger.debug(f'Initializing the MassUpload ttk frame.')

        style = ttk.Style()
        style.configure('TRadiobutton', font=('Helvetica', 15))
        style.configure('TCheckbutton', font=('Helvetica', 14))

        self.aws = AWS()

        # Check if program is running through the .app or from direct python
        if 'Resources' in os.getcwd():
            self.open_folder_icon_path = tk.PhotoImage(file=os.getcwd() + '/images/open_folder_icon.png')
            logger.debug(f'Retrieving image "{os.getcwd()}/images/open_folder_icon.png"')

            self.refresh_button_image = tk.PhotoImage(file=os.getcwd() + '/images/refresh_icon.png')
            logger.debug(f'Retrieving image "{os.getcwd()}/images/refresh_icon.png"')
        else:
            self.open_folder_icon_path = tk.PhotoImage(
                file=os.getcwd() + '/S3_File_Uploader/UI/images/open_folder_icon.png')
            logger.debug(f'Retrieving image "{os.getcwd()}/S3_File_Uploader/UI/images/open_folder_icon.png"')

            self.refresh_button_image = tk.PhotoImage(file=os.getcwd() + '/S3_File_Uploader/UI/images/refresh_icon.png')
            logger.debug(f'Retrieving image "{os.getcwd()}/S3_File_Uploader/UI/images/refresh_icon.png"')

        self.S3_BUCKET_VALUES = self.aws.get_s3_buckets()

        self._ui_elements()
        logger.debug(f'Created MassUpload UI elements.')

        self.radio_button_var.set(1)

    def _ui_elements(self):
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

        self.overall_progressbar_label = ttk.Label(
            self,
            text='Total Progress',
            font=('Helvetica', 13),
            justify=tk.CENTER
        )

        # Row 2 is a progressbar that is created when needed

        # Row 3
        self.ffmpeg_and_upload_progressbar_label = ttk.Label(
            self,
            text='',
            font=('Helvetica', 13),
            justify=tk.CENTER
        )

        # Row 4 is a progressbar that is created when needed

        # Row 5
        self.path_to_mass_upload_label = ttk.Label(
            self,
            text='Directory path for mass upload:',
            font=('Helvetica', 15),
            justify=tk.CENTER
        )
        self.path_to_mass_upload_label.grid(
            self.PATH_TO_MASS_UPLOAD_LABEL_GRID)

        # Row 6
        self.mass_upload_path = tk.StringVar()
        self.mass_upload_path_input_field = ttk.Entry(
            self,
            width=35,
            textvariable=self.mass_upload_path
        )
        self.mass_upload_path_input_field.grid(
            self.MASS_UPLOAD_PATH_INPUT_FIELD_GRID)

        self.mass_upload_path_button = ttk.Button(
            self,
            image=self.open_folder_icon_path,
            command=self._open_folder_path
        )
        self.mass_upload_path_button.grid(self.MASS_UPLOAD_PATH_BUTTON_GRID)

        # Row 7
        self.s3_bucket_location_label = ttk.Label(
            self,
            text='Please select the S3 bucket to upload to:',
            font=('Helvetica', 15),
            justify=tk.CENTER
        )
        self.s3_bucket_location_label.grid(self.S3_BUCKET_LOCATION_LABEL_GRID)

        # Row 8
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
            command=self._refresh_s3_buckets
        )
        self.refresh_s3_buckets_button.grid(
            self.REFRESH_S3_BUCKETS_BUTTON_GRID)

        # Row 9
        self.radio_button_label = ttk.Label(
            self,
            text='Please select what type file to upload:',
            font=('Helvetica', 15),
            justify=tk.CENTER
        )
        self.radio_button_label.grid(self.RADIO_BUTTON_LABEL_GRID)

        # Row 10
        self.radio_button_var = tk.IntVar()

        self.radio_button_all = ttk.Radiobutton(
            self,
            text="All Files",
            value=1,
            variable=self.radio_button_var,
            command=self._all_files_radio_active
        )
        self.radio_button_all.grid(self.RADIO_BUTTON_ALL_GRID)

        self.radio_button_video = ttk.Radiobutton(
            self,
            text="Videos Only",
            value=2,
            variable=self.radio_button_var,
            command=self._video_only_radio_active
        )
        self.radio_button_video.grid(self.RADIO_BUTTON_VIDEO_GRID)

        # self.radio_button_audio = ttk.Radiobutton(
        #     self,
        #     text='Audio Only',
        #     value=3,
        #     variable=self.radio_button_var,
        #     command=self._audio_only_radio_active
        # )
        # self.radio_button_audio.grid(self.RADIO_BUTTON_AUDIO_GRID)

        # Row 11 & 12
        self.video_checkboxes = VideoCheckboxes(
            self,
            self.controller
        )

        # Row 13
        self.use_ffmpeg_checkbox_var = tk.IntVar()
        self.use_ffmpeg_checkbox = ttk.Checkbutton(
            self,
            text="Use FFMPEG",
            variable=self.use_ffmpeg_checkbox_var
        )

        # Row 14
        self.start_upload_button = ttk.Button(
            self,
            text='Start Upload',
            style='regular.TButton',
            command=self.start_upload
        )
        self.start_upload_button.grid(self.START_UPLOAD_BUTTON_GRID)

    def _open_folder_path(self):
        """ Function that runs when the open folder button is clicked. """
        logger.debug('Opening file dialog window for selecting local save path.')

        path = filedialog.askdirectory()
        self.mass_upload_path.set(path)

        logger.debug(f'Setting local save path to: "{path}"')

    def _refresh_s3_buckets(self):
        """ Function that runs when the refresh button is clicked. """
        logger.debug(f'Refreshing S3 buckets.')

        self.update_label.configure(text='')

        s3_bucket_values = self.aws.get_s3_buckets()
        self.s3_bucket_selector.configure(values=s3_bucket_values)

        self.update_label.configure(
            text='S3 buckets updated',
            foreground='#3fe03f'  # Darker green
        )

    def _all_files_radio_active(self):
        logger.debug(f'All files radio button is selected.')

        # When the All files radio button is clicked,
        #   then the video checkboxes and the use ffmpeg checkbox
        #   are removed from the grid.
        # Then the use ffmpeg checkbox variable is set to 0
        #   so that it doesn't say selected when not needed.
        self.video_checkboxes.grid_forget()
        self.use_ffmpeg_checkbox.grid_forget()
        self.use_ffmpeg_checkbox_var.set(0)

    def _video_only_radio_active(self):
        logger.debug(f'Video only radio button is selected.')

        # Add the VideoCheckboxes frame
        self.video_checkboxes.grid(self.VIDEO_FORMAT_GRID)

        # Add the use FFMPEG checkbox
        self.use_ffmpeg_checkbox.grid(self.USE_FFMPEG_GRID)

    def _audio_only_radio_active(self):
        logger.debug(f'Audio only radio button is selected.')

        self.video_checkboxes.grid_forget()
        self.use_ffmpeg_checkbox.grid_forget()
        self.use_ffmpeg_checkbox_var.set(0)

    def _create_overall_progressbar(self, number_of_files):
        """ Function to remove the update label from the grid and add the overall progressbar and label to grid.

        Args:
            number_of_files (int): The number of files in the directory that will be uploaded.
                                   This is used as the maximum value of the progressbar.
        """
        logger.debug(f'Creating overall progressbar with a maximum of `{str(number_of_files)}`.')

        # Remove the update label from the grid so that a progress bar can go instead
        self.update_label.grid_remove()

        # Add the overall label over the progressbar
        self.overall_progressbar_label.grid(self.OVERALL_PROGRESSBAL_LABEL_GRID)

        # Create the overall progressbar and add it to the grid
        self.overall_pb = ProgressBar(self, self.controller, 400, number_of_files)
        self.overall_pb.grid(self.OVERALL_PROGRESSBAR_GRID)

    def _destroy_overall_progressbar(self):
        """ Function to remove the overall progressbar from grid and add the update label. """
        logger.debug(f'Destroying overall progressbar.')

        self.overall_progressbar_label.grid_remove()
        self.overall_pb.grid_remove()
        self.update_label.grid(self.UPDATE_LABEL_GRID)

    def _create_ffmpeg_and_upload_progressbar(self, length_of_bar):
        """ Function to add the secondary progressbar that is used to track ffmpeg and upload progress to grid.

        Args:
            length_of_bar (int): The maximum value for the secondary progressbar.
                                 This is either the number of frames that will be converted using FFMPEG,
                                 or the total size of the file that will be uploaded.
        """
        logger.debug(f'Creating secondary (ffmpeg & upload) progressbar with a maximum of `{length_of_bar}`')

        self.ffmpeg_and_upload_progressbar_label.grid(self.FFMPEG_AND_UPLOAD_PROGRESSBAR_LABEL_GRID)
        self.ffmpeg_and_upload_pb = ProgressBar(self, self.controller, 400, length_of_bar)
        self.ffmpeg_and_upload_pb.grid(self.FFMPEG_AND_UPLOAD_PROGRESSBAR_GRID)

    def _destroy_ffmpeg_and_upload_progressbar(self):
        """ Function to remove the secondary progressbar from grid. """
        logger.debug(f'Destroying secondary (ffmpeg & upload) progressbar.')

        self.ffmpeg_and_upload_progressbar_label.grid_remove()
        self.ffmpeg_and_upload_pb.grid_remove()

    @staticmethod
    def _parse_ffmpeg_command(ffmpeg_config, input_file_path, input_file_name, input_file_extension):
        """ Function to parse together the FFMPEG command to a string.

        This function parses together the FFMPEG command from that data the user entered on the setup page,
        and returns that command as well as the converted file path and name.

        Args:
            ffmpeg_config (list): The list output from the database. The data the user entered on the setup page.
            input_file_path (str): The path to the file that will be converted.
            input_file_name (str): The file name of the file that will be converted
            input_file_extension (str): The extension of the file that will be converted.

        Returns:
            ffmpeg_command_string (str): The parsed together string of the ffmpeg commad
            first_full_output_string (str): A string with the converted file path and name.
        """
        logger.debug(f'Creating string with ffmpeg command.')

        # Doing this so that it is more readable than `ffmpeg_config[0]...`
        ffmpeg_parameters, file_suffix, aws_different_output_extension, local_save_path, local_different_output_extension = ffmpeg_config

        # Create a string with the full input file
        full_input_string = input_file_path
        full_input_string += '/' if input_file_path[-1] != '/' else ''
        full_input_string += input_file_name
        full_input_string += f'.{input_file_extension}'

        ffmpeg_parameters = ffmpeg_parameters if ffmpeg_parameters is not None else ''

        # Create first output file
        output_file_name = input_file_name
        first_output_extension = aws_different_output_extension if aws_different_output_extension is not None else input_file_extension

        first_full_output_string = f'{input_file_path}/{output_file_name}{file_suffix}.{first_output_extension}'

        # Setup the ffmpeg command for one output
        ffmpeg_command_string = f'ffmpeg -i "{full_input_string}" {ffmpeg_parameters} -y "{first_full_output_string}"'

        # Check if there needs to be a second output
        if local_save_path is not None:
            ffmpeg_command_string += f' {local_save_path}/'

            # Check if using a different output extension for the local save
            if local_different_output_extension is not None:
                second_output_file = f'{output_file_name}{file_suffix}.{local_different_output_extension}'
            else:
                second_output_file = f'{output_file_name}.{first_output_extension}'

            ffmpeg_command_string += f'"{second_output_file}"'

        logger.debug(f'Ffmpeg command string created: `{ffmpeg_command_string}`.')

        return ffmpeg_command_string, first_full_output_string

    def _ffmpeg_controller(self, parsed_ffmpeg_command, ffmpeg_progressbar, total_video_frames: int):
        """ Function to run FFMPEG using the parsed ffmpeg command.

        Args:
            parsed_ffmpeg_command (str): The string with the full ffmpeg command that was parsed using the `_parse_ffmpeg_command` function.
            ffmpeg_progressbar (ttk.Progressbar): Progressbar to show the ffmpeg progress.
            total_video_frames (int): The total frames of the file that will be converted. This is used as the maximum value for the progressbar.
        """
        logger.debug(f'Starting ffmpeg conversion using command: `{parsed_ffmpeg_command}`.')

        # Reset progressbar
        ffmpeg_progressbar.change_progressbar_maximum(total_video_frames)
        ffmpeg_progressbar.reset_progressbar_value()

        # Change secondary progressbar label
        self.ffmpeg_and_upload_progressbar_label.configure(
            text='FFMPEG Progress')

        # subprocess.run(
        #     parsed_ffmpeg_command.split(),
        #     stdout=subprocess.DEVNULL,
        #     stderr=subprocess.DEVNULL
        # )

        # Create a new thread running the parsed ffmpeg command
        thread = pexpect.spawn(parsed_ffmpeg_command)

        # Compile a patters of what to to look for in the stdout.
        # In this case, the number next to `frame=`.
        cpl = thread.compile_pattern_list([
            pexpect.EOF,
            "frame= *\d+",
            '(.+)'
        ])

        # While the command is running, check the thread for the compiled pattern
        while True:
            i = thread.expect_list(cpl, timeout=None)

            # If there is no line output (the program finished), then break out of the loop
            if i == 0:  # EOF
                # print("the sub process exited")
                break

            # If there is output, and that output contains the compiled string,
            #   then the frame number will be changed from byte code to string
            #   then from string to integer to update the progressbar with the frame.
            elif i == 1:
                frame_number = thread.match.group(0)

                frame_num = str(
                    frame_number, 'utf-8').replace('frame=', '').lstrip()

                logger.debug(f'Updating ffmpeg progressbar.')
                ffmpeg_progressbar.update_progressbar_value(int(frame_num))

                thread.close

        logger.debug(f'Ffmpeg conversion completed.')

    def _ffprobe_controller(full_file_name: str) -> int:
        """ Function to run the ffprobe command to get the number of frames in the video.

        Args:
            full_file_name (str): Full path and file name to ffprobe.

        Returns:
            int: Number of frames in the video
        """
        command = f'ffprobe -count_frames -select_streams v:0 -show_entries stream=nb_frames "{full_file_name}"'

        logger.debug(f'Retrieving video frames using command: {command}')

        thread = pexpect.spawn(command)

        cpl = thread.compile_pattern_list([
            pexpect.EOF,
            'nb_frames=\d+',
            '(.+)'
        ])

        frames = "0"

        while True:
            i = thread.expect_list(cpl, timeout=None)
            if i == 0:
                break
            elif i == 1:
                frames = thread.match.group(0)
                thread.close

        number_of_frames = str(frames, 'utf-8').replace('nb_frames=', '')

        logger.debug(f'Returning number of frames: `{number_of_frames}`')

        return int(number_of_frames)

    def start_upload(self):
        logger.debug(f'Start Upload button pressed.')

        logger.debug(f'Disabling widgets.')
        self.disable_widgets()

        # Check if there already was an upload started but didn't finish
        with Database() as DB:
            not_finished_mass_upload = DB.get_mass_upload_not_ended_data()

        if not_finished_mass_upload:
            logger.debug(f'There was a mass upload that did not finish.')

            upload_id, mass_upload_path, \
                s3_bucket, upload_type, use_ffmpeg = not_finished_mass_upload[0]

            nw = NotFinishedWindow(
                controller=self.controller,
                not_finished_data=not_finished_mass_upload[0]
            )
            nw.grab_set()
            self.wait_window(nw)

            user_input_button = nw.retrieve_button_pressed()

            if user_input_button is None:
                return

            if user_input_button == 'n':
                with Database() as DB:
                    DB.finish_mass_upload()
                pass

            if user_input_button == 'y':
                logger.debug(f'Filling in previous mass upload data on ttk widgets.')

                self.mass_upload_path.set(mass_upload_path)
                self.s3_bucket_name.set(s3_bucket)

                if upload_type == 'all':
                    self.radio_button_var.set(1)
                else:
                    self.radio_button_var.set(2)
                    self.video_checkboxes.set_checkbox(upload_type)
                    self.use_ffmpeg_checkbox_var.set(use_ffmpeg)

                self.resume_mass_upload(not_finished_mass_upload[0])
                return

        logger.debug(f'Retrieving all user entered data.')
        # Get the data from what the user added
        mass_upload_starting_path = self.mass_upload_path.get()
        bucket_name = self.s3_bucket_name.get()
        radio_button = self.radio_button_var.get()

        logger.debug(f'Retrieving number of files in selected source directory.')
        number_of_files = sum(
            [len(files) for r, d, files in os.walk(mass_upload_starting_path)]
        )

        # Dictionary with the file/directory as key and Byte size as value
        #  from AWS bucket. (Used to not overwrite file that is already in the bucket)
        bucket_objects_dict = self.aws.get_bucket_objects_as_dict(bucket_name)

        # If the All Files radio button is selected
        if radio_button == 1:
            with Database() as DB:
                DB.add_mass_upload_data(
                    mass_upload_path=mass_upload_starting_path,
                    s3_bucket=bucket_name,
                    upload_type='all',
                    use_ffmpeg=0
                )

            self._create_overall_progressbar(number_of_files)

            logger.debug(f'Starting a new thread for `start_mass_upload_all`.')
            # Start a new thread calling start_mass_upload_all()
            self.mass_upload_all_thread = threading.Thread(
                target=self.start_mass_upload_all,
                args=(
                    mass_upload_starting_path,
                    bucket_name,
                    bucket_objects_dict
                )
            )
            self.mass_upload_all_thread.start()

        # If the Video Only radio button is selected
        elif radio_button == 2:
            logger.debug(f'Retrieving the video checkbox selection.')
            # Get the checkboxes that are selected
            video_checkbox_selection = [
                a for a in self.video_checkboxes.state()]

            with Database() as DB:
                all_video_formats_labels = DB.get_video_formats(labels=True)

            selected_video_format_labels = []
            selected_video_formats = []

            with Database() as DB:
                for checkbox, format in zip(video_checkbox_selection, all_video_formats_labels):
                    if checkbox == 1:
                        selected_video_format_labels.append(format)

                        for vf in DB.get_video_formats(False, format):
                            selected_video_formats.append(vf)

            logger.debug(f'Retrieve if use ffmpeg checkbox is selected.')
            # Check if using FFMPEG or not
            use_ffmpeg = self.use_ffmpeg_checkbox_var.get()

            # Add the mass upload data to the database
            with Database() as DB:
                DB.add_mass_upload_data(
                    mass_upload_path=mass_upload_starting_path,
                    s3_bucket=bucket_name,
                    upload_type=','.join(selected_video_format_labels),
                    use_ffmpeg=use_ffmpeg
                )

            self._create_overall_progressbar(number_of_files)

            logger.debug(f'Starting a new thread for `start_mass_upload_video`.')
            threading.Thread(
                target=self.start_mass_upload_video,
                args=(
                    mass_upload_starting_path,
                    bucket_name,
                    bucket_objects_dict,
                    selected_video_formats,
                    use_ffmpeg
                )
            ).start()

        # If the Audio Only radio button is selected
        # elif radio_button == 3:  # Audio only
        #     print('audio selected')

    def start_mass_upload_all(self, upload_start_path,
                              bucket_name, bucket_objects_dict):
        logger.debug(f'Starting mass upload for all files.')

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
                    self.overall_pb.step()
                    continue

                with Database() as DB:
                    DB.add_file_upload(
                        dirpath, file, file_size_from_pc, bucket_name)

                self.aws.upload_file(
                    full_path_from_pc, bucket_name, full_bucket_path)

                with Database() as DB:
                    DB.finish_file_upload(dirpath, file)

                self.overall_pb.step()

        # Finishing upload
        with Database() as DB:
            DB.finish_mass_upload()

        # Remove the progressbar from grid and re-add the update label
        #   letting the user know that the upload finished.
        self._destroy_overall_progressbar()
        self.update_label.configure(text='Finished!', foreground='black')

        logger.debug(f'Mass upload finished.')
        logger.debug(f'Enabling widgets.')
        self.enable_widgets()

    def start_mass_upload_video(self, upload_start_path, bucket_name,
                                bucket_objects_dict, video_formats_to_use, use_ffmpeg):
        logger.debug(f'Starting mass upload for video files.')

        ffmpeg_config = []
        if use_ffmpeg:
            logger.debug(f'Program will be using ffmpeg to convert the video file before uploading to AWS S3.')
            with Database() as DB:
                ffmpeg_config = DB.get_ffmpeg_config()

            # Create secondary progressbar only if it uses ffmpeg
            self._create_ffmpeg_and_upload_progressbar(100)

        # Get the position of the actual folder that will get uploaded
        length_to_remove = upload_start_path.rfind('/') + 1

        # Iterate through the upload directory
        for dirpath, dirnames, filenames in os.walk(upload_start_path):
            # Get the directory path that is used for S3
            bucket_dir_path = dirpath[length_to_remove:] + '/'

            # Iterate through all the files in the directory
            for file in filenames:
                logger.debug(f'Current file in loop: {file}')
                # Get the file extension for the iterated file
                file_extension_start = str(file).rfind('.') + 1
                file_extension = file[file_extension_start:]

                # If the file extension isn't one of the `video_formats_to_use` list
                #   then the progressbar will step up and the file will not be uploaded
                if file_extension not in video_formats_to_use:
                    logger.debug(f'Current file is not a video, skipping file.')
                    self.overall_pb.step()
                    continue

                # If use_ffmpeg is true then convert the file first
                #   then upload that converted file
                if use_ffmpeg:
                    # Get file size of the non-converted (original) file
                    # If this is a resume upload, then there will be an extra
                    #   converted file that is non-existant but the os.walk
                    #   loop thinks is there.
                    # So this has to be surrounded by
                    #   a try/except clause
                    try:
                        logger.debug(f'Trying to retrieve file size of the original file.')

                        original_file_byte_size = int(
                            os.path.getsize(dirpath + '/' + file))
                    except FileNotFoundError:
                        logger.error(f'FileNotFoundError exception caught for file: `{dirpath}/{file}`.')

                        logger.error(f'Continuing to the next file.')
                        self.overall_pb.step()
                        continue

                    # Parse together the ffmpeg command and return the command alongside the new
                    #   file path and name
                    parsed_ffmpeg_command, converted_file_path_and_name = self._parse_ffmpeg_command(
                        ffmpeg_config, dirpath, file[:file.rfind('.')], file[file.rfind('.') + 1:])

                    # Get a separate file path and name for the converted video
                    converted_file_path = converted_file_path_and_name[
                        :converted_file_path_and_name.rfind('/')]
                    converted_file_name = converted_file_path_and_name[
                        converted_file_path_and_name.rfind('/') + 1:]

                    full_bucket_path = bucket_dir_path + converted_file_name

                    # Check if the current iterated file has already been converted and
                    #   uploaded to AWS.
                    # If it is, then add one to the overall progressbar and continue
                    #   to the next iteration
                    with Database() as DB:
                        # This checks if the file was converted and uploaded on the database
                        #  but also check if the file is currently in AWS
                        # If either is false, then the file will get converted and uploaded
                        if DB.is_file_already_converted_and_uploaded(
                                dirpath, file, original_file_byte_size, bucket_name) \
                                and full_bucket_path in bucket_objects_dict:

                            self.overall_pb.step()
                            logger.debug(f'Skipping file since it was already converted and uploaded: {dirpath}/{file}')
                            continue

                    # Get the Frames of the video to use for the ffmpeg progressbar
                    try:
                        logger.debug(f'Trying to run ffprobe through `ffmpeg-python` module.')
                        total_video_frames = ffmpeg.probe(f"{dirpath}/{file}")['streams'][0]['nb_frames']
                    except Exception as e:
                        logger.warning(f"ffprobe exception occurred: {e}.")

                        try:
                            logger.debug(f'Trying to run ffprobe command.')
                            total_video_frames = self._ffprobe_controller(f"{dirpath}/{file}")
                        except Exception as e:
                            logger.warning(f"Secondary ffprobe exception occurred: {e}\nSkipping ffprobe.")
                            total_video_frames = 10000

                    # Run the FFMPEG program
                    self._ffmpeg_controller(
                        parsed_ffmpeg_command,
                        self.ffmpeg_and_upload_pb,
                        total_video_frames
                    )

                    # Get the file size of the converted video file
                    # Have to use a try/except clause since some NAS create a hidden file
                    #   that the program tries to use but isn't really there.
                    try:
                        logger.debug(f'Trying to retrieve file size of converted file.')

                        converted_file_byte_size = int(os.path.getsize(converted_file_path_and_name))
                    except FileNotFoundError as e:
                        logger.error(f'FileNotFoundError exception caught for file: `{converted_file_path_and_name}`.')

                        logger.error(f'Continuing to the next file.')
                        print(f"File not found: '{converted_file_path_and_name}'.\nSkipping file.\n")
                        self.overall_pb.step()
                        continue

                    # Add the FFMPEG converted data to the database
                    with Database() as DB:
                        DB.add_ffmpeg_conversion(
                            dirpath, file, original_file_byte_size,
                            converted_file_path, converted_file_name,
                            converted_file_byte_size
                        )

                    # Now that the FFMPEG conversion is done, need to reset the secondary
                    #  progressbar for aws upload
                    self.ffmpeg_and_upload_progressbar_label.configure(text='S3 Upload Progress')
                    self.ffmpeg_and_upload_pb.reset_progressbar_value()

                    self.ffmpeg_and_upload_pb.change_progressbar_maximum(converted_file_byte_size)
                    logger.debug(f'Switching secondary progressbar for S3 upload progress.')

                    # Add file upload to database
                    with Database() as DB:
                        DB.add_file_upload(
                            converted_file_path,
                            converted_file_name,
                            converted_file_byte_size,
                            bucket_name
                        )

                    # Upload converted file to AWS
                    self.aws.upload_file(
                        converted_file_path_and_name,
                        bucket_name,
                        full_bucket_path,
                        S3UploadProgress(self.ffmpeg_and_upload_pb)
                    )

                    # Finish finalize the file upload in the database
                    with Database() as DB:
                        DB.finish_file_upload(
                            converted_file_path, converted_file_name
                        )

                    # Delete the converted file
                    os.remove(converted_file_path_and_name)
                    logger.debug(f'Removing converted file that was uploaded to AWS.')

                    self.overall_pb.step()

                    logger.debug(f'Continuing to the next file.')
                    continue

                # Not using ffmpeg
                full_path_from_pc = dirpath + '/' + file
                full_bucket_path = bucket_dir_path + file

                logger.debug(f'Getting file size of file.')
                file_size_from_pc = os.path.getsize(full_path_from_pc)

                # If the file is already in the bucket (with the same byte size),
                #   then the loop will continue.
                if full_bucket_path in bucket_objects_dict \
                        and file_size_from_pc == bucket_objects_dict[full_bucket_path]:
                    logger.debug(f'Current file with the same name and file size is already in AWS S3, skipping file.')
                    self.overall_pb.step()
                    continue

                with Database() as DB:
                    DB.add_file_upload(
                        dirpath,
                        file,
                        file_size_from_pc,
                        bucket_name
                    )

                self.aws.upload_file(
                    full_path_from_pc,
                    bucket_name,
                    full_bucket_path
                )

                with Database() as DB:
                    DB.finish_file_upload(dirpath, file)

                self.overall_pb.step()
                logger.debug(f'Continuing to the next file.')

        # Finishing upload, all files have been iterated through
        with Database() as DB:
            DB.finish_mass_upload()

        # Remove the progressbar from grid and re-add the update label
        #   letting the user know that the upload finished.
        self._destroy_overall_progressbar()
        if use_ffmpeg:
            self._destroy_ffmpeg_and_upload_progressbar()

        self.update_label.configure(text='Finished!', foreground='black')
        logger.debug(f'Changing text to `finished` to let user know that the upload is complete.')

        logger.debug(f'Enabling widgets.')
        self.enable_widgets()

    def resume_mass_upload(self, not_finished_data):
        logger.debug(f'Starting resume mass upload.')

        logger.debug(f'Disabling widgets.')
        self.disable_widgets()

        upload_id, mass_upload_path, s3_bucket, upload_type, use_ffmpeg = not_finished_data

        bucket_objects_dict = self.aws.get_bucket_objects_as_dict(s3_bucket)

        number_of_files = sum([len(files) for r, d, files in os.walk(mass_upload_path)])

        self._create_overall_progressbar(number_of_files)

        if upload_type == 'all':
            logger.debug(f'Starting a new thread with the `start_mass_upload_all` function.')

            threading.Thread(
                target=self.start_mass_upload_all,
                args=(
                    mass_upload_path,
                    s3_bucket,
                    bucket_objects_dict
                )
            ).start()
        else:
            video_checkbox_selection = upload_type.split(',')

            selected_video_formats = []

            with Database() as DB:
                for checkbox in video_checkbox_selection:
                    for vf in DB.get_video_formats(False, checkbox):
                        selected_video_formats.append(vf)

            logger.debug(f'Starting a new thread with the `start_mass_upload_video` function.')
            threading.Thread(
                target=self.start_mass_upload_video,
                args=(
                    mass_upload_path,
                    s3_bucket,
                    bucket_objects_dict,
                    selected_video_formats,
                    use_ffmpeg
                )
            ).start()

    def disable_widgets(self):
        logger.debug(f'Disabling all main window buttons.')
        self.controller.disable_main_window_buttons()

        logger.debug(f'Disabling all the MassUpload window widgets.')

        self.mass_upload_path_input_field.configure(state='disabled')
        self.mass_upload_path_button.configure(state='disabled')
        self.s3_bucket_selector.configure(state='disabled')
        self.refresh_s3_buckets_button.configure(state='disabled')
        self.radio_button_all.configure(state='disabled')
        self.radio_button_video.configure(state='disabled')
        self.use_ffmpeg_checkbox.configure(state='disabled')
        self.start_upload_button.configure(state='disabled')

        # Since the video checkboxes is a different class,
        # then the class has to have functions for disablind and unbinding
        self.video_checkboxes.disable_all_widgets()
        self.video_checkboxes.unbind_widgets()

    def enable_widgets(self):
        logger.debug(f'Enabling all main window buttons.')
        self.controller.enable_main_window_buttons()

        logger.debug(f'Enabling all the MassUpload window widgets.')

        self.mass_upload_path_input_field.configure(state='normal')
        self.mass_upload_path_button.configure(state='normal')
        self.s3_bucket_selector.configure(state='readonly')
        self.refresh_s3_buckets_button.configure(state='normal')
        self.radio_button_all.configure(state='normal')
        self.radio_button_video.configure(state='normal')
        self.use_ffmpeg_checkbox.configure(state='normal')
        self.start_upload_button.configure(state='normal')

        # Since the video checkboxes is a different class,
        # then the class has to have functions for disablind and unbinding
        self.video_checkboxes.enable_all_widgets()
        self.video_checkboxes.bind_widgets()


class VideoCheckboxes(ttk.Frame):
    def __init__(self, parent, controller):
        logger.debug(f'Initializing VideoCheckboxes ttk frame.')

        ttk.Frame.__init__(self, parent, relief=tk.FLAT)
        self.controller = controller

        self.checkbox_text = ''
        self.checkbox_variables = []
        self.checkbox_text_and_variables = []

        with Database() as DB:
            self.checkbox_text = DB.get_video_formats(labels=True)

        logger.debug(f'Creating checkboxes.')
        for i, text_ in enumerate(self.checkbox_text):
            var = tk.IntVar()

            var.set(1)

            checkbox = ttk.Checkbutton(
                self,
                text=text_,
                variable=var
            )
            checkbox.grid(row=0, column=i, padx=2)

            self.checkbox_variables.append(var)
            self.checkbox_text_and_variables.append(tuple([text_, var]))

        logger.debug(f'Creating hover text label.')
        self.hover_text = ttk.Label(
            self,
            text='',
            font=('Helvetica', 14, 'italic'),
            justify=tk.CENTER
        )
        self.hover_text.grid(row=1, column=0, columnspan=len(self.checkbox_text), pady=(3, 0))

        # Bind the checkbox widgets to update the hover text label
        self.bind_widgets()

    def set_checkbox(self, checkbox_label: List[str]) -> None:
        for checkbox in self.checkbox_text_and_variables:
            if checkbox[0] in checkbox_label:
                checkbox[1].set(1)
            else:
                checkbox[1].set(0)

    def state(self):
        """ Returns a map of 0 or 1 for which video extension checkbox is selected. """
        logger.debug(f'Returning a map of which video extension is select/not selected.')
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

    def disable_all_widgets(self):
        logger.debug(f'Disabling all checkboxes.')
        for child in self.winfo_children():
            child.configure(state='disabled')

    def enable_all_widgets(self):
        logger.debug(f'Enabling all checkboxes.')
        for child in self.winfo_children():
            child.configure(state='enable')

    def unbind_widgets(self):
        logger.debug(f'Unbinding all checkboxes.')
        for child in self.winfo_children():
            child.unbind("<Enter>")
            child.unbind("<Leave>")

    def bind_widgets(self):
        logger.debug(f'Binding all checkboxes.')
        for child in self.winfo_children():
            if "checkbutton" in child.widgetName:
                child.bind("<Enter>", self.enter_bind)
                child.bind("<Leave>", self.leave_bind)


class ProgressBar(ttk.Frame):
    def __init__(self, parent, controller, bar_size, number_of_steps):
        logger.debug(f'Initializing Progressbar.')

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

    def change_progressbar_maximum(self, maximum):
        self.progressbar.configure(maximum=maximum)

    def reset_progressbar_value(self):
        self.var.set(0)

    def update_progressbar_value(self, value):
        # Have to update the variable and not the actual value of progressbar.
        # For some reason this is the only way to make it work.
        self.var.set(value)


class NotFinishedWindow(tk.Toplevel):
    def __init__(self, controller, not_finished_data):
        logger.debug(f'Creating NotFinishedWindow.')
        tk.Toplevel.__init__(self, controller)
        self.controller = controller
        self.not_finished_data = not_finished_data

        self.no_button_pressed = False
        self.yes_button_pressed = False

        self.resizable(False, False)

        frame = ttk.Frame(
            self,
            relief=tk.RIDGE
        )
        frame.grid()

        top_level = ttk.Label(
            frame,
            text="There was a mass upload that didn't finish. Do you want to continue this upload?"
        )
        top_level.grid(row=0, column=0, columnspan=2, pady=15, padx=40)

        upload_path = ttk.Label(
            frame,
            text=f'Upload directory: {self.not_finished_data[1]}'
        )
        upload_path.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        bucket = ttk.Label(
            frame,
            text=f'S3 Bucket: {self.not_finished_data[2]}'
        )
        bucket.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        no_button = ttk.Button(
            frame,
            text='NO',
            command=self.no_button_press
        )
        no_button.grid(row=3, column=0, pady=10, padx=10)

        yes_button = ttk.Button(
            frame,
            text='YES',
            command=self.yes_button_press
        )
        yes_button.grid(row=3, column=1, pady=10, padx=10)

        # Center the window
        screen_x, screen_y = controller.get_screen_size()

        windowWidth = self.winfo_reqwidth()
        windowHeight = self.winfo_reqheight()

        positionRight = int(screen_x/2 - windowWidth/2)
        positionDown = int(screen_y/2 - windowHeight/2)

        self.geometry(f"+{positionRight}+{positionDown}")

    def no_button_press(self):
        self.no_button_pressed = True
        # self.controller.full_opacity()
        self.destroy()

    def yes_button_press(self):
        self.yes_button_pressed = True
        # self.controller.full_opacity()
        self.destroy()

    def retrieve_button_pressed(self):
        if self.no_button_pressed:
            return 'n'
        elif self.yes_button_pressed:
            return 'y'


class S3UploadProgress(object):
    def __init__(self, progressbar):
        logger.debug(f'Initializing S3UploadProgress.')
        self._progressbar = progressbar
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        logger.debug(f'Updating S3UploadProgress progressbar')
        with self._lock:
            self._seen_so_far += int(bytes_amount)
            self._progressbar.update_progressbar_value(self._seen_so_far)
