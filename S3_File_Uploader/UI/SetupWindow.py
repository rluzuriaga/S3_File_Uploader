import logging
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

import os
import threading

from Database import Database
from AWS import AWS, AWSAuthenticationException, AWSKeyException, NoConnectionError

# Set up logging
logger = logging.getLogger('main_logger')


class SetupWindow(ttk.Frame):
    # Row 0
    TOP_LABEL_GRID = {'row': 0, 'column': 0, 'columnspan': 4, 'padx': 280, 'pady': (15, 15)}

    # Row 1
    OUTPUT_MESSAGE_GRID = {'row': 1, 'column': 0, 'columnspan': 4, 'pady': (5, 5)}

    # Row 2
    AWS_HEADING_GRID = {'row': 2, 'column': 0, 'columnspan': 4, 'pady': (5, 1)}

    # Row 3
    ACCESS_KEY_ID_LABEL_GRID = {'row': 3, 'column': 0, 'columnspan': 2, 'padx': (25, 0), 'pady': (10, 0), 'sticky': 'w'}
    ACCESS_KEY_ID_INPUT_GRID = {'row': 3, 'column': 2, 'columnspan': 2, 'padx': (5, 25), 'pady': (10, 0), 'sticky': 'e'}

    # Row 4
    SECRET_KEY_LABEL_GRID = {'row': 4, 'column': 0, 'columnspan': 2, 'padx': (25, 0), 'pady': (10, 0), 'sticky': 'w'}
    SECRET_KEY_INPUT_GRID = {'row': 4, 'column': 2, 'columnspan': 2, 'padx': (5, 25), 'pady': (10, 0), 'sticky': 'e'}

    # Row 5
    REGION_NAME_LABEL_GRID = {'row': 5, 'column': 0, 'columnspan': 2, 'padx': (25, 0), 'pady': (10, 20), 'sticky': 'w'}
    REGION_NAME_INPUT_GRID = {'row': 5, 'column': 2, 'columnspan': 2, 'padx': (5, 25), 'pady': (10, 20), 'sticky': 'e'}

    # Row 6
    FFMPEG_HEADING_LABEL_GRID = {'row': 6, 'column': 0, 'columnspan': 4, 'pady': (5, 1)}

    # Row 7
    FFMPEG_INPUT_LABEL_GRID = {'row': 7, 'column': 0, 'columnspan': 2, 'padx': (25, 0), 'pady': (10, 0), 'sticky': 'w'}
    FFMPEG_INPUT_GRID = {'row': 7, 'column': 2, 'columnspan': 2, 'padx': (22, 25), 'pady': (10, 0), 'sticky': 'w'}

    # Row 8
    CONVERTED_FILE_SUFFIX_LABEL_GRID = {'row': 8, 'column': 0, 'columnspan': 2,
                                        'padx': (25, 0), 'pady': (10, 0), 'sticky': 'w'}
    CONVERTED_FILE_SUFFIX_INPUT_GRID = {'row': 8, 'column': 2, 'columnspan': 2,
                                        'padx': (22, 25), 'pady': (10, 0), 'sticky': 'w'}

    # Row 9
    DIFFERENT_EXTENSION_CHECKBOX_GRID = {'row': 9, 'column': 0,
                                         'columnspan': 2, 'padx': (25, 0), 'pady': (10, 0), 'sticky': 'w'}
    DIFFERENT_EXTENSION_INPUT_GRID = {'row': 9, 'column': 2,
                                      'columnspan': 2, 'padx': (22, 25), 'pady': (10, 0), 'sticky': 'w'}

    # Row 10
    LOCAL_SAVE_CHECKBOX_GRID = {'row': 10, 'column': 0, 'columnspan': 2,
                                'padx': (25, 0), 'pady': (10, 0), 'sticky': 'w'}
    LOCAL_SAVE_PATH_INPUT_GRID = {'row': 10, 'column': 2, 'padx': (22, 5), 'pady': (10, 0), 'sticky': 'w'}
    LOCAL_SAVE_PATH_BUTTON_GRID = {'row': 10, 'column': 3, 'padx': (0, 20), 'pady': (10, 0)}

    # Row 11
    LOCAL_SAVE_OUTPUT_EXTENSION_CHECKBOX_GRID = {'row': 11, 'column': 0,
                                                 'columnspan': 2, 'padx': (25, 0), 'pady': (10, 0), 'sticky': 'w'}
    LOCAL_SAVE_OUTPUT_EXTENSION_INPUT_GRID = {'row': 11, 'column': 2,
                                              'columnspan': 2, 'padx': (22, 25), 'pady': (10, 0), 'sticky': 'w'}

    # Row 12
    FFMPEG_EXAMPLE_LABEL = {'row': 12, 'column': 0, 'columnspan': 4, 'pady': (2, 0)}

    # Row 13
    SAVE_BUTTON_GRID = {'row': 13, 'column': 0, 'columnspan': 2, 'pady': (20, 10)}
    LOCK_UNLOCK_BUTTON_GRID = {'row': 13, 'column': 2, 'columnspan': 2,
                               'padx': (0, 40), 'pady': (20, 10), 'sticky': 'E'}

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent, width=100,
                           height=300, relief=tk.RIDGE)
        self.controller = controller

        logger.debug('Initializing the SetupWindow ttk frame.')

        style = ttk.Style()
        style.configure('regular.TButton', font=('Helvetica', 15))
        style.configure('regular.TCheckbutton', font=('Helvetica', 15))

        if 'Resources' in os.getcwd():
            self.open_folder_icon_path = tk.PhotoImage(
                file=os.getcwd() + '/images/open_folder_icon.png')
            logger.debug(f'Retrieving image "{os.getcwd()}/images/open_folder_icon.png"')
        else:
            self.open_folder_icon_path = tk.PhotoImage(
                file=os.getcwd() + '/S3_File_Uploader/UI/images/open_folder_icon.png')
            logger.debug(f'Retrieving image "{os.getcwd()}/S3_File_Uploader/UI/images/open_folder_icon.png"')

        self.ui_elements()
        logger.debug("Created SetupWindow UI elements.")

        self.populate_setup_fields()

    def ui_elements(self):
        # Row 0
        self.setup_window_top_label = ttk.Label(
            self,
            text='Please enter all the data.',
            font=('Helvetica', 15),
            justify=tk.CENTER
        )
        self.setup_window_top_label.grid(self.TOP_LABEL_GRID)

        # Row 1
        self.setup_window_output_message = ttk.Label(
            self,
            text='',
            font=('Helvetica', 15),
            justify=tk.CENTER
        )
        self.setup_window_output_message.grid(self.OUTPUT_MESSAGE_GRID)

        # Row 2
        self.aws_heading_label = ttk.Label(
            self,
            text='AWS Settings',
            font=('Helvetica', 15, 'bold', 'underline'),
            justify=tk.CENTER
        )
        self.aws_heading_label.grid(self.AWS_HEADING_GRID)

        # Row 3
        self.access_key_id_label = ttk.Label(
            self,
            text='AWS Access Key ID:',
            font=('Helvetica', 15),
            justify=tk.LEFT
        )
        self.access_key_id_label.grid(self.ACCESS_KEY_ID_LABEL_GRID)

        self.access_key_id_string = tk.StringVar()
        self.access_key_id_input_field = ttk.Entry(
            self,
            width=44,
            textvariable=self.access_key_id_string
        )
        self.access_key_id_input_field.grid(self.ACCESS_KEY_ID_INPUT_GRID)

        # Row 4
        self.secret_key_label = ttk.Label(
            self,
            text='AWS Secret Access Key:',
            font=('Helvetica', 15),
            justify=tk.LEFT
        )
        self.secret_key_label.grid(self.SECRET_KEY_LABEL_GRID)

        self.secret_key_string = tk.StringVar()
        self.secret_key_input_field = ttk.Entry(
            self,
            width=44,
            textvariable=self.secret_key_string
        )
        self.secret_key_input_field.grid(self.SECRET_KEY_INPUT_GRID)

        # Row 5
        self.region_name_label = ttk.Label(
            self,
            text='Default Region Name:',
            font=('Helvetica', 15),
            justify=tk.LEFT
        )
        self.region_name_label.grid(self.REGION_NAME_LABEL_GRID)

        with Database() as DB:
            region_labels = DB.get_region_name_labels()

        self.region_name_var = tk.StringVar()
        self.region_name_input_field = ttk.Combobox(
            self,
            textvariable=self.region_name_var,
            values=region_labels,
            width=42,
            state='readonly'
        )
        self.region_name_input_field.grid(self.REGION_NAME_INPUT_GRID)

        # Row 6
        self.ffmpeg_heading_label = ttk.Label(
            self,
            text='FFMPEG Settings',
            font=('Helvetica', 15, 'bold', 'underline'),
            justify=tk.CENTER
        )
        self.ffmpeg_heading_label.grid(self.FFMPEG_HEADING_LABEL_GRID)

        # Row 7
        self.ffmpeg_input_label = ttk.Label(
            self,
            text='FFMPEG parameters: ',
            font=('Helvetica', 15),
            justify=tk.LEFT
        )
        self.ffmpeg_input_label.grid(self.FFMPEG_INPUT_LABEL_GRID)

        self.ffmpeg_input_var = tk.StringVar()
        self.ffmpeg_input_var.set('-b:v 64k -bufsize 64k')
        self.ffmpeg_input = ttk.Entry(
            self,
            width=44,
            textvariable=self.ffmpeg_input_var
        )
        self.ffmpeg_input.grid(self.FFMPEG_INPUT_GRID)

        # Row 8
        self.converted_file_suffix_label = ttk.Label(
            self,
            text='Converted file suffix:',
            font=('Helvetica', 15),
            justify=tk.LEFT
        )
        self.converted_file_suffix_label.grid(self.CONVERTED_FILE_SUFFIX_LABEL_GRID)

        self.converted_file_suffix_input_var = tk.StringVar()
        self.converted_file_suffix_input_var.set('_converted')
        self.converted_file_suffix_input = ttk.Entry(
            self,
            width=20,
            textvariable=self.converted_file_suffix_input_var
        )
        self.converted_file_suffix_input.grid(self.CONVERTED_FILE_SUFFIX_INPUT_GRID)

        # Row 9
        self.use_different_extension = tk.IntVar()
        self.different_ffmpeg_output_extension_checkbutton = ttk.Checkbutton(
            self,
            text='Different output extension for AWS',
            variable=self.use_different_extension,
            style='regular.TCheckbutton',
            command=self._ffmpeg_extension_checkbutton_press
        )
        self.different_ffmpeg_output_extension_checkbutton.grid(
            self.DIFFERENT_EXTENSION_CHECKBOX_GRID)

        self.different_output_extension_var = tk.StringVar()
        self.different_output_extension_var.set("avi")
        self.different_ffmpeg_output_extension_input = ttk.Entry(
            self,
            width=10,
            textvariable=self.different_output_extension_var
        )

        # Row 10
        self.local_save_var = tk.IntVar()
        self.local_save_checkbox = ttk.Checkbutton(
            self,
            text='Save locally',
            variable=self.local_save_var,
            style='regular.TCheckbutton',
            command=self._local_save_press
        )
        self.local_save_checkbox.grid(self.LOCAL_SAVE_CHECKBOX_GRID)

        self.local_save_path_var = tk.StringVar()
        self.local_save_path_input_field = ttk.Entry(
            self,
            width=36,
            textvariable=self.local_save_path_var
        )

        self.local_save_path_button = ttk.Button(
            self,
            image=self.open_folder_icon_path,
            command=self._open_folder_path
        )

        # Row 11
        self.local_save_different_extension_checkbox_var = tk.IntVar()
        self.local_save_different_extension_checkbox = ttk.Checkbutton(
            self,
            text='Different local output extension',
            variable=self.local_save_different_extension_checkbox_var,
            style='regular.TCheckbutton',
            command=self._local_save_different_extension_press
        )

        self.local_save_different_output_extension_input_var = tk.StringVar()
        self.local_save_different_output_extension_input_var.set("mkv")
        self.local_save_different_output_extension_input = ttk.Entry(
            self,
            width=10,
            textvariable=self.local_save_different_output_extension_input_var
        )

        # Row 12
        self.ffmpeg_example_label = ttk.Label(
            self,
            text='',
            font=('Helvetica', 13),
            justify=tk.CENTER
        )
        self.ffmpeg_example_label.grid(self.FFMPEG_EXAMPLE_LABEL)

        # Row 13
        self.save_button = ttk.Button(
            self,
            text="Save Configuration",
            style='regular.TButton',
            command=self.save_configuration
        )
        self.save_button.grid(self.SAVE_BUTTON_GRID)

        self.lock_unlock_button = ttk.Button(
            self,
            text='Lock',
            style='regular.TButton',
            command=self.lock_unlock_aws_settings,
            # Disabled since there should be nothing saved on the database at first boot
            state='disabled'
        )
        self.lock_unlock_button.grid(self.LOCK_UNLOCK_BUTTON_GRID)

    def _open_folder_path(self):
        logger.debug('Opening file dialog window for selecting local save path.')
        path = filedialog.askdirectory()
        self.local_save_path_var.set(path)
        logger.debug(f'Setting local save path to: "{path}"')

    def _update_ffmpeg_data(self):
        """ Function to update the example ffmpeg label.

        The function puts together the label with the user entered options, 
        then call the Tkinter after() function to update the label every 3/4 second (750 ms).
        """
        # If the user also wants to have the new files locally saved, then an extra output
        # is added to the example label
        if self.local_save_different_extension_checkbox_var.get():
            text_ = 'Example: ffmpeg -i input.avi ' + \
                    self.ffmpeg_input_var.get() + \
                    ' output.' + \
                    self.different_output_extension_var.get() + \
                    ' output.' + \
                    self.local_save_different_output_extension_input_var.get()
        else:
            text_ = 'Example: ffmpeg -i input.avi ' + \
                    self.ffmpeg_input_var.get() + \
                    ' output.' + \
                    self.different_output_extension_var.get()

        self.ffmpeg_example_label.configure(text=text_)

        # If this needs to be changed in the future, make sure that the variable
        #   is an instance variable so that there is only one after() thread.
        # I used to have this function return the variable and the issue with that
        #   was that a thread was created every 750 milliseconds.
        self.after_id = self.ffmpeg_input.after(750, self._update_ffmpeg_data)

    def _ffmpeg_extension_checkbutton_press(self):
        """ Function that runs when the `Use different extension for AWS` checkbox is pressed.

        The function adds and removes the `different_ffmpeg_output_extension_input` entry box
        depending on if the checkbox is selected or not.
        """
        # If the checkbox is selected, then the Entry box is added to the grid
        # If not, then the Entry box is removed from the grid and the output extension
        #  is set to 'avi' so that the example label has the correct value.
        if self.use_different_extension.get():
            self.different_ffmpeg_output_extension_input.grid(self.DIFFERENT_EXTENSION_INPUT_GRID)
            logger.debug('Adding the `different output extension` entry box to the grid.')
        else:
            self.different_ffmpeg_output_extension_input.grid_remove()
            self.different_output_extension_var.set("avi")
            logger.debug('Removing the `different output extension` entry box from the grid.')

    def _local_save_press(self):
        """ Function that runs when the `Save locally` checkbox is pressed.

        The function adds and removes the local save path Entry box and button to 
        the grid depending on if the `Save locally` checkbox is selected or not.
        """
        # If the checkbox is selected, the local save path Entry box, button, and the
        #  different local extension checkbox are added to the grid.
        # If it is unchecked, then those are removed from the grid.
        if self.local_save_var.get():
            self.local_save_path_input_field.grid(self.LOCAL_SAVE_PATH_INPUT_GRID)
            self.local_save_path_button.grid(self.LOCAL_SAVE_PATH_BUTTON_GRID)
            self.local_save_different_extension_checkbox.grid(self.LOCAL_SAVE_OUTPUT_EXTENSION_CHECKBOX_GRID)
            logger.debug('Adding the `local save` input field, button and different extension checkbox to the grid.')
        else:
            self.local_save_path_input_field.grid_remove()
            self.local_save_path_button.grid_remove()
            self.local_save_different_extension_checkbox.grid_remove()

            self.local_save_different_output_extension_input.grid_remove()
            logger.debug('Removing the `local save` input field, button and different extension checkbox from the grid.')

    def _local_save_different_extension_press(self):
        """ Function that runs when the `Different local output extension` checkbox is pressed.

        The function adds and removes the Entry box for the different local output extension
        to the grid depending on if the checkbox is selected or not.
        """
        # If the checkbox is selected, then the Entry box is added to the grid.
        # If the checkbox is not selected, then the Entry box is removed from the grid.
        if self.local_save_different_extension_checkbox_var.get():
            self.local_save_different_output_extension_input.grid(self.LOCAL_SAVE_OUTPUT_EXTENSION_INPUT_GRID)
            logger.debug('Adding the local save different extension to the grid.')
        else:
            self.local_save_different_output_extension_input.grid_remove()
            logger.debug('Removing the local save different extension from the grid.')

    def _disable_all_widgets(self):
        """ Function to disable all of the input widgets in the SetupWindow. """
        # AWS widgets
        self.access_key_id_input_field.configure(state='disabled', foreground='gray')
        self.secret_key_input_field.configure(state='disabled', foreground='gray')
        self.region_name_input_field.configure(state='disabled', foreground='gray')
        logger.debug('Disabling the AWS input fields.')

        # FFMPEG widgets
        self.ffmpeg_input.configure(state='disabled', foreground='gray')

        self.converted_file_suffix_input.configure(state='disabled', foreground='gray')

        self.different_ffmpeg_output_extension_checkbutton.configure(state='disabled')
        self.different_ffmpeg_output_extension_input.configure(state='disabled', foreground='grey')

        self.local_save_checkbox.configure(state='disabled')
        self.local_save_path_input_field.configure(state='disabled', foreground='grey')
        self.local_save_path_button.configure(state='disabled')

        self.local_save_different_extension_checkbox.configure(state='disabled')
        self.local_save_different_output_extension_input.configure(state='disabled', foreground='grey')
        logger.debug('Disabling the FFMPEG input fields.')

    def _enable_all_widgets(self):
        """ Function to enable all of the input widgets in the SetupWindow. """
        # AWS options
        self.access_key_id_input_field.configure(state='normal', foreground='black')
        self.secret_key_input_field.configure(state='normal', foreground='black')
        self.region_name_input_field.configure(state='readonly', foreground='black')
        logger.debug('Enabling the AWS input fields.')

        # FFMPEG options
        self.ffmpeg_input.configure(state='normal', foreground='black')

        self.converted_file_suffix_input.configure(state='normal', foreground='black')

        self.different_ffmpeg_output_extension_checkbutton.configure(state='normal')
        self.different_ffmpeg_output_extension_input.configure(state='normal', foreground='black')

        self.local_save_checkbox.configure(state='normal')
        self.local_save_path_input_field.configure(state='normal', foreground='black')
        self.local_save_path_button.configure(state='normal')

        self.local_save_different_extension_checkbox.configure(state='normal')
        self.local_save_different_output_extension_input.configure(state='normal', foreground='black')
        logger.debug('Enabling the FFMPEG input fields.')

    def start_after(self):
        """ Function to activate the method that updates the FFMPEG example label.

        This function is created so that it can be called when the SetupWindow pane 
        is active instead of at all time. This makes it so that the program isn't 
        trying to update something the user isn't needing every 750 milliseconds.
        """
        self._update_ffmpeg_data()
        logger.debug('Starting the tkinter after() method for updating the example ffmpeg text.')

    def stop_after(self):
        """ Function to cancel the method that updates the FFMPEG example label.

        This function is created so that it can be called when the SetupWindow pane 
        is active instead of at all time. This makes it so that the program isn't 
        trying to update something the user isn't needing every 750 milliseconds.
        """
        self.ffmpeg_input.after_cancel(self.after_id)
        logger.debug('Stopping the tkinter after() method.')

    def save_configuration(self):
        """ Function that runs when the `Save Configuration` button is pressed. """
        logger.debug('Starting save configuration process.')

        self.setup_window_output_message.configure(text='')

        # Get AWS input data
        access_key_id = self.access_key_id_input_field.get()
        secret_key = self.secret_key_input_field.get()
        region_name = self.region_name_var.get()

        # Get FFMPEG input data
        ffmpeg_parameters = self.ffmpeg_input_var.get()

        use_different_output_extension_for_aws = self.use_different_extension.get()
        output_extension_for_aws = self.different_output_extension_var.get()

        use_local_save = self.local_save_var.get()
        local_save_path = self.local_save_path_var.get()

        use_different_output_extension_for_local = self.local_save_different_extension_checkbox_var.get()
        output_extension_for_local = self.local_save_different_output_extension_input_var.get()

        # Check if the user checked the "Different output extension for AWS" box but didn't
        #  input the extension in the entry box.
        # If so, then an error message is displayed.
        if use_different_output_extension_for_aws and output_extension_for_aws == '':
            self.setup_window_output_message.configure(
                text='The output extension for AWS cannot be empty.', foreground='red')
            logger.warning('No extension entered when the `Different output extension for AWS`checkbox was selected.')
            return

        # Check if the user checked the "Save locally" box but didn't input
        #  the path in the entry box.
        # If so, then an error message is displayed.
        if use_local_save and local_save_path == '':
            self.setup_window_output_message.configure(
                text='The local save path cannot be empty.', foreground='red')
            logger.warning('No local save path entered when the `Save locally` checkbox was selected.')
            return

        # Check if the user checked the "Different local output extension" box but didn't
        # input the extension in the entry box.
        # If so, then an error message is displayed.
        if use_different_output_extension_for_local and output_extension_for_local == '':
            self.setup_window_output_message.configure(
                text='The local output extension cannot be empty.', foreground='red')
            logger.warning('No extension entered when the `Different local output extension` checkbox was selected.')
            return

        with Database() as DB:
            # Since SQLite3 requires text values to be surrounded in single quotes
            # when executing an SQL statement,
            # I have to do this hack to get the single quotes around the string variable
            # or pass "NULL" if it's not needed
            DB.set_ffmpeg_config(
                ffmpeg_parameters,
                "'{}'".format(
                    output_extension_for_aws) if use_different_output_extension_for_aws else "NULL",
                "'{}'".format(local_save_path) if use_local_save else "NULL",
                "'{}'".format(
                    output_extension_for_local) if use_different_output_extension_for_local else "NULL"
            )

        # If any of the AWS inputs is empty, then a message is given
        # Else, a configuration message is given and a new thread is created
        #   to test and save the AWS connection
        if access_key_id == '' or secret_key == '' or region_name == '':
            self.setup_window_output_message.configure(
                text='All AWS fields must to be filled in.', foreground='red')
            logger.warning('Not all AWS fields are filled in.')
        else:
            self.setup_window_output_message.configure(
                text='Configuring AWS settings. Please wait.', foreground='black')

            threading.Thread(
                target=self.configure_aws,
                args=(access_key_id, secret_key, region_name)
            ).start()

    def configure_aws(self, access_key_id, secret_key, region_name):
        """ Function to configure AWS settings.

        This function should be ran on another thread so that the UI elements are
        not stuck.

        Args:
            access_key_id (str): User inputted Access Key ID for AWS.
            secret_key (str): User inputted Secret Key for AWS.
            region_name (str): User selected region name from list.

        Raises:
            AWSAuthenticationException: Exception is raised when the HTTP Status Code 
                from AWS is not 200.

        Catches:
            AWSKeyException: Exception is caught when either the Access Key ID or the 
                Secret Key are wrong.
            AWSAuthenticationException: Exception is caught when the Access Key ID and 
                Secret Key are correct but seem to be inactive.
            NoConnectionError: Exception is caught when there is no Internet connection.
        """
        with Database() as DB:
            try:
                region_name_code = DB.get_region_name_code(region_name)

                response = AWS.test_connection(
                    access_key_id, secret_key, region_name_code)

                if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                    DB.set_aws_config(
                        access_key_id, secret_key, region_name_code)

                    self.setup_window_output_message.configure(text='')
                    self.setup_window_output_message.configure(
                        text='Settings saved.', foreground='#3fe03f')  # Darker green than foreground='green'

                    self.lock_unlock_button.configure(state='normal')

                    # Enable all main window buttons
                    self.controller.enable_main_window_buttons()

                    # Run function to lock the settings
                    self.lock_unlock_aws_settings()
                else:
                    raise AWSAuthenticationException
            except AWSKeyException:
                self.setup_window_output_message.configure(
                    text='ERROR: Access Key ID or Secret Access Key invalid.', foreground='red')
                logger.error('ERROR: Invalid AWS Access Key ID or Secret Access Key entered.')
            except AWSAuthenticationException:
                self.setup_window_output_message.configure(
                    text='ERROR: Keys are correct but they may be inactive.', foreground='red')
                logger.error('ERROR: Innactive AWS keys entered.')
            except NoConnectionError:
                self.setup_window_output_message.configure(
                    text='ERROR: No Internet connection detected.', foreground='red')
                logger.error('ERROR: No Internet connection, cannot authenticate AWS keys.')

    def lock_unlock_aws_settings(self):
        """ This function executes when the 'Lock/Unlock' button is clicked. """
        with Database() as DB:

            # If there is an AWS config already saved in the database,
            # then the program checks if the button says 'Lock' or 'Unlock'
            # If there is no data on the database, then the 'Lock/Unlock' button is disabled
            # and enables the save button
            if DB.are_settings_saved():

                # If the button says 'Lock', then the input fields are disabled, the
                # text is grayed out, the save button is removed, and the button is
                # renamed to 'Unlock'
                if self.lock_unlock_button['text'] == 'Lock':
                    logger.debug('Configuration window locked.')

                    self._disable_all_widgets()

                    self.lock_unlock_button['text'] = 'Unlock'

                    self.save_button.grid_remove()

                # If the button says 'Unlock', then the input fields are editable, the
                # text is changed to black, the save button is added to the screen, and
                # the button is renamed to 'Lock'
                elif self.lock_unlock_button['text'] == 'Unlock':
                    logger.debug('Configuration window unlocked.')

                    self._enable_all_widgets()

                    self.lock_unlock_button['text'] = 'Lock'

                    self.save_button.grid(self.SAVE_BUTTON_GRID)
            else:
                self.lock_unlock_button.configure(
                    text='Lock', state='disabled')
                self.save_button.grid(self.SAVE_BUTTON_GRID)

    def populate_setup_fields(self):
        """ Populate the setup fields with the information from the database. 

        This function checks if there are settings saved in the database. 
            - If there are, then the function will add all those settings into 
            the entry boxes the data corresponds to.
            - If there are no settings saved on the database, then the function
            doesn't do anything to the fields.
        """
        with Database() as DB:
            if DB.are_settings_saved():
                logger.debug('Populating setup fields with data from the database.')

                # AWS settings
                aws_config_data = DB.get_aws_config(label=True)

                self.access_key_id_string.set(aws_config_data[0])
                self.secret_key_string.set(aws_config_data[1])
                self.region_name_var.set(aws_config_data[2])

                # FFMPEG settings
                ffmpeg_parameters, aws_different_output_extension, local_save_path, local_different_output_extension = DB.get_ffmpeg_config()

                # Set the ffmpeg_parameters data into the entry box,
                # if there is data for that in the database.
                # If there is no data (it's NULL), then an empty string is added to the entry box.
                self.ffmpeg_input_var.set(
                    ffmpeg_parameters if ffmpeg_parameters is not None else ""
                )

                # If the database's `aws_different_output_extension` field is NULL/None,
                # then the different_ffmpeg_output_extension_checkbutton is unchecked
                if aws_different_output_extension is None:
                    self.use_different_extension.set(0)

                # If that field is not NULL/None, then the
                # different_ffmpeg_output_extension_checkbutton is checked,
                # the extension is set to the entry box, and the entry box is
                # added to the grid.
                else:
                    self.use_different_extension.set(1)
                    self.different_output_extension_var.set(
                        aws_different_output_extension)

                    self.different_ffmpeg_output_extension_input.grid(
                        self.DIFFERENT_EXTENSION_INPUT_GRID)

                # If the database's `local_save_path` field is NULL/None,
                # then the local_save_checkbox is unchecked
                if local_save_path is None:
                    self.local_save_var.set(0)

                # If that field is not NULL/None, then the
                # local_save_checkbox is checked, the path is set to the entry field,
                # and the entry box and button is added to the grid.
                else:
                    self.local_save_var.set(1)
                    self.local_save_path_var.set(local_save_path)

                    self.local_save_path_input_field.grid(
                        self.LOCAL_SAVE_PATH_INPUT_GRID)
                    self.local_save_path_button.grid(
                        self.LOCAL_SAVE_PATH_BUTTON_GRID)

                # If the database's `local_different_output_extension` field is NULL/None,
                # then the local_save_different_extension_checkbox is unchecked
                if local_different_output_extension is None:
                    self.local_save_different_extension_checkbox_var.set(0)

                # If that field is not NULL/None, then the
                # local_save_different_extension_checkbox is checked, the extension is
                # added to the entry box, and the checkbox and entry box are added to the grid.
                else:
                    self.local_save_different_extension_checkbox_var.set(1)
                    self.local_save_different_output_extension_input_var.set(
                        local_different_output_extension)

                    self.local_save_different_extension_checkbox.grid(
                        self.LOCAL_SAVE_OUTPUT_EXTENSION_CHECKBOX_GRID)
                    self.local_save_different_output_extension_input.grid(
                        self.LOCAL_SAVE_OUTPUT_EXTENSION_INPUT_GRID)

                # After adding all the data to the page then all the widgets are disabled
                # and the screen is displayed as if the Lock button was pressed.
                self._disable_all_widgets()
                self.lock_unlock_button['text'] = 'Unlock'
                self.lock_unlock_button.configure(state='normal')

                self.save_button.grid_remove()
