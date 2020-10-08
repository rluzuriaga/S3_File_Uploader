import tkinter as tk
from tkinter import ttk
import threading

from Database import Database
from AWS import AWS, AWSAuthenticationException, AWSKeyException, NoConnectionError

class SetupWindow(ttk.Frame):
    TOP_LABEL_GRID = {'row': 0, 'column': 0, 'columnspan': 2, 'padx': 200, 'pady': (15, 15)}
    OUTPUT_MESSAGE_GRID = {'row': 1, 'column': 0, 'columnspan': 2, 'pady': (5, 5)}

    AWS_HEADING_GRID = {'row': 2, 'column': 0, 'columnspan': 2, 'pady': (5, 1)}

    # Left labels
    ACCESS_KEY_ID_LABEL_GRID = {'row': 3, 'column': 0, 'columnspan': 1, 'padx': (30, 0), 'pady': (10, 0), 'sticky': 'w'}
    SECRET_KEY_LABEL_GRID = {'row': 4, 'column': 0, 'columnspan': 1, 'padx': (30, 0), 'pady': (10, 0), 'sticky': 'w'}
    REGION_NAME_LABEL_GRID = {'row': 5, 'column': 0, 'columnspan': 1, 'padx': (30, 0), 'pady' :(10, 0), 'sticky':'w'}

    # Data input fields
    ACCESS_KEY_ID_INPUT_GRID = {'row': 3, 'column': 1, 'columnspan': 1, 'padx': (0, 30), 'pady': (10, 0), 'sticky': 'e'}
    SECRET_KEY_INPUT_GRID = {'row': 4, 'column': 1, 'columnspan': 1, 'padx': (0, 30), 'pady': (10, 0), 'sticky': 'e'}
    REGION_NAME_INPUT_GRID = {'row': 5, 'column': 1, 'columnspan': 1, 'padx': (0, 30), 'pady': (10, 0), 'sticky': 'e'}

    # Buttons
    SAVE_BUTTON_GRID = {'row': 6, 'column': 0, 'pady': (20, 10)}
    LOCK_UNLOCK_BUTTON_GRID = {'row': 6, 'column': 1, 'padx': (0, 40), 'pady': (20, 10), 'sticky': 'E'}

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent, width=100, height=300, relief=tk.RIDGE)
        self.controller = controller

        style = ttk.Style()
        style.configure('regular.TButton', font=('Helvetica', 15))
    
        self.ui_elements()
        self.populate_setup_fields()

    def ui_elements(self):
        self.setup_window_top_label = ttk.Label(
            self,
            text='Please enter all the data.',
            font=('Helvetica', 15),
            justify=tk.CENTER
        )
        self.setup_window_top_label.grid(self.TOP_LABEL_GRID)

        # Label to get the user output messages like failed or success
        self.setup_window_output_message = ttk.Label(
            self,
            text='',
            font=('Helvetica', 15),
            justify=tk.CENTER
        )
        self.setup_window_output_message.grid(self.OUTPUT_MESSAGE_GRID)

        self.aws_heading_label = ttk.Label(
            self,
            text='AWS Settings',
            font=('Helvetica', 15, 'bold', 'underline'),
            justify=tk.CENTER,
        )
        self.aws_heading_label.grid(self.AWS_HEADING_GRID)

        # Left labels
        self.access_key_id_label = ttk.Label(
            self,
            text='AWS Access Key ID:',
            font=('Helvetica', 15),
            justify=tk.LEFT
        )
        self.access_key_id_label.grid(self.ACCESS_KEY_ID_LABEL_GRID)

        self.secret_key_label = ttk.Label(
            self,
            text='AWS Secret Access Key:',
            font=('Helvetica', 15),
            justify=tk.LEFT
        )
        self.secret_key_label.grid(self.SECRET_KEY_LABEL_GRID)

        self.region_name_label = ttk.Label(
            self,
            text='Default Region Name:',
            font=('Helvetica', 15),
            justify=tk.LEFT
        )
        self.region_name_label.grid(self.REGION_NAME_LABEL_GRID)


        # Data input fields
        self.access_key_id_string = tk.StringVar()
        self.access_key_id_input_field = ttk.Entry(
            self,
            width=44,
            textvariable=self.access_key_id_string
        )
        self.access_key_id_input_field.grid(self.ACCESS_KEY_ID_INPUT_GRID)

        self.secret_key_string = tk.StringVar()
        self.secret_key_input_field = ttk.Entry(
            self,
            width=44,
            textvariable=self.secret_key_string
        )
        self.secret_key_input_field.grid(self.SECRET_KEY_INPUT_GRID)

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
        self.region_name_input_field.grid(self.REGION_NAME_INPUT_GRID)


        # Buttons
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

    # When the 'Save Configuration' button is pressed
    def save_configuration(self):
        self.setup_window_output_message.configure(text='')

        # Get all input data
        self.access_key_id = self.access_key_id_input_field.get()
        self.secret_key = self.secret_key_input_field.get()
        self.region_name = self.region_name_input_field.get()

        # The get command removes the selection from the screen
        # So this put's it back on the screen
        self.region_name_input_field.set(self.region_name)

        # If any of the inputs is empty, then a message is given
        # Else, a configuration message is given and a new thread is created
        #   to test and save the AWS connection
        if self.access_key_id == '' or self.secret_key == '' or self.region_name == '':
            self.setup_window_output_message.configure(text='All fields must to be filled in.', foreground='red')
        else:
            self.setup_window_output_message.configure(text='Configuring AWS settings. Please wait.', foreground='black')
            
            threading.Thread(
                target=self.configure_aws,
                args=(self.access_key_id, self.secret_key, self.region_name)
            ).start()
    
    def configure_aws(self, access_key_id, secret_key, region_name):
        with Database() as DB:
            try:
                region_name_code = DB.get_region_name_code(region_name)

                response = AWS.test_connection(access_key_id, secret_key, region_name_code)

                if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                    DB.set_aws_config(access_key_id, secret_key, region_name_code)

                    self.setup_window_output_message.configure(text='')
                    self.setup_window_output_message.configure(text='AWS settings saved.', foreground='#3fe03f') # Darker green than foreground='green'

                    self.lock_unlock_button.configure(state='normal')

                    # Enable all main window buttons
                    self.controller.enable_main_window_buttons()
                else:
                    raise AWSAuthenticationException
            except AWSKeyException:
                self.setup_window_output_message.configure(text='ERROR: Access Key ID or Secret Access Key invalid.', foreground='red')
            except AWSAuthenticationException:
                self.setup_window_output_message.configure(text='ERROR: Keys are correct but they may be inactive.', foreground='red')
            except NoConnectionError:
                self.setup_window_output_message.configure(text='ERROR: No Internet connection detected.', foreground='red')

    # When the 'Lock/Unlock' button is clicked
    def lock_unlock_aws_settings(self):
        """ This function executes when the 'Lock/Unlock' button is clicked. """
        with Database() as DB:

            # If there is an AWS config already saved in the database,
            # then the program checks if the button says 'Lock' or 'Unlock'
            # If there is no data on the database, then the 'Lock/Unlock' button is disabled
            # and enables the save button
            if DB.is_aws_config_saved():

                # If the button says 'Lock', then the input fields are disabled, the 
                # text is grayed out, the save button is removed, and the button is 
                # renamed to 'Unlock'
                if self.lock_unlock_button['text'] == 'Lock':
                    self.access_key_id_input_field.configure(state='disabled', foreground='gray')
                    self.secret_key_input_field.configure(state='disabled', foreground='gray')
                    self.region_name_input_field.configure(state='disabled', foreground='gray')

                    self.lock_unlock_button['text'] = 'Unlock'

                    self.save_button.grid_remove()

                # If the button says 'Unlock', then the input fields are editable, the
                # text is changed to black, the save button is added to the screen, and
                # the button is renamed to 'Lock'
                elif self.lock_unlock_button['text'] == 'Unlock':
                    self.access_key_id_input_field.configure(state='normal', foreground='black')
                    self.secret_key_input_field.configure(state='normal', foreground='black')
                    self.region_name_input_field.configure(state='readonly', foreground='black')

                    self.lock_unlock_button['text'] = 'Lock'

                    self.save_button.grid(self.SAVE_BUTTON_GRID)
            else:
                self.lock_unlock_button.configure(text='Lock', state='disabled')
                self.save_button.grid(self.SAVE_BUTTON_GRID)
    
    def populate_setup_fields(self):
        """ Pupulated the setup fields with the info from the database. """
        with Database() as DB:
            if DB.is_aws_config_saved():
                aws_config_data = DB.get_aws_config(label=True)
                self.access_key_id_string.set(aws_config_data[0])
                self.secret_key_string.set(aws_config_data[1])
                self.region_name.set(aws_config_data[2])

                self.access_key_id_input_field.configure(state='disabled', foreground='gray')
                self.secret_key_input_field.configure(state='disabled', foreground='gray')
                self.region_name_input_field.configure(state='disabled', foreground='gray')

                self.lock_unlock_button['text'] = 'Unlock'
                self.lock_unlock_button.configure(state='normal')

                self.save_button.grid_remove()
