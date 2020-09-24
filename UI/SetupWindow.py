import tkinter as tk
from tkinter import ttk
import threading

from Database import Database
from AWS import AWS, AWSAuthenticationException, AWSKeyException, NoConnectionError

class SetupWindow(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent, width=100, height=300, relief=tk.RIDGE)
        self.controller = controller

        style = ttk.Style()
        style.configure('regular.TButton', font=('Helvetica', 15))
    
        self.ui_elements()

    def ui_elements(self):
        self.setup_window_top_label = ttk.Label(
            self,
            text='Please enter all the data.',
            font=('Helvetica', 15),
            justify=tk.CENTER
        )
        self.setup_window_top_label.grid(row=0, column=0, columnspan=2, padx=200, pady=(15, 15))

        # Label to get the user output messages like failed or success
        self.setup_window_output_message = ttk.Label(
            self,
            text='',
            font=('Helvetica', 15),
            justify=tk.CENTER
        )
        self.setup_window_output_message.grid(row=1, column=0, columnspan=2, pady=(5, 5))

        self.aws_heading_label = ttk.Label(
            self,
            text='AWS Settings',
            font=('Helvetica', 15, 'bold', 'underline'),
            justify=tk.CENTER,
        )
        self.aws_heading_label.grid(row=2, column=0, columnspan=2, pady=(5, 1))

        # Left labels
        self.access_key_id_label = ttk.Label(
            self,
            text='AWS Access Key ID:',
            font=('Helvetica', 15),
            justify=tk.LEFT
        )
        self.access_key_id_label.grid(row=3, column=0, columnspan=1, padx=(30, 0), pady=(10, 0), sticky='w')

        self.secret_key_label = ttk.Label(
            self,
            text='AWS Secret Access Key:',
            font=('Helvetica', 15),
            justify=tk.LEFT
        )
        self.secret_key_label.grid(row=4, column=0, columnspan=1, padx=(30, 0), pady=(10, 0), sticky='w')

        self.region_name_label = ttk.Label(
            self,
            text='Default Region Name:',
            font=('Helvetica', 15),
            justify=tk.LEFT
        )
        self.region_name_label.grid(row=5, column=0, columnspan=1, padx=(30, 0), pady=(10, 0), sticky='w')


        # Data input fields
        self.access_key_id_string = tk.StringVar()
        self.access_key_id_input_field = ttk.Entry(
            self,
            width=44,
            textvariable=self.access_key_id_string
        )
        self.access_key_id_input_field.grid(row=3, column=1, columnspan=1, padx=(0, 30), pady=(10, 0), sticky='e')

        self.secret_key_string = tk.StringVar()
        self.secret_key_input_field = ttk.Entry(
            self,
            width=44,
            textvariable=self.secret_key_string
        )
        self.secret_key_input_field.grid(row=4, column=1, columnspan=1, padx=(0, 30), pady=(10, 0), sticky='e')

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
        self.region_name_input_field.grid(row=5, column=1, columnspan=1,padx=(0, 30), pady=(10, 0), sticky='e')


        # Buttons
        self.save_button = ttk.Button(
            self,
            text="Save Configuration",
            style='regular.TButton',
            command=self.save_configuration
        )
        self.save_button.grid(row=6, column=0, pady=(20, 10))

        self.lock_unlock_button = ttk.Button(
            self,
            text='Lock',
            style='regular.TButton',
            command=lambda: print('lock unlock'),
            # Disabled since there should be nothing saved on the database at first boot
            state='disabled'
        )
        self.lock_unlock_button.grid(row=6, column=1, padx=(0, 40), pady=(20, 10), sticky='E')

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
                else:
                    raise AWSAuthenticationException
            except AWSKeyException:
                self.setup_window_output_message.configure(text='ERROR: Access Key ID or Secret Access Key invalid.', foreground='red')
            except AWSAuthenticationException:
                self.setup_window_output_message.configure(text='ERROR: Keys are correct but they may be inactive.', foreground='red')
            except NoConnectionError:
                self.setup_window_output_message.configure(text='ERROR: No Internet connection detected.', foreground='red')
