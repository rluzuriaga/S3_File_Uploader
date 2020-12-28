import sys
from tkinter import ttk


class Styles:
    def __init__(self) -> None:
        if 'darwin' in sys.platform:
            self._is_mac = True
            self._is_window = False
        elif 'win' in sys.platform:
            self._is_mac = False
            self._is_window = True

        self.style = ttk.Style()

        self.all_ui_styles()
        self.main_window_styles()
        self.setup_window_styles()
        self.update_database_styles()

    def all_ui_styles(self) -> None:
        if self._is_mac:
            self.style.configure('regular.TButton', font=('Helvetica', 15))
            self.style.configure('regular.TCheckbutton', font=('Helvetica', 15))

        if self._is_window:
            self.style.configure('regular.TButton', font=('Helvetica', 12))
            self.style.configure('regular.TCheckbutton', font=('Helvetica', 12))

    def main_window_styles(self) -> None:
        if self._is_mac:
            self.style.configure('main_window_top_label.TLabel', font=('Helvetica', 15))
            self.style.configure('main_window_statusbar.TLabel', font=('Helvetica', 10))

        if self._is_window:
            self.style.configure('main_window_top_label.TLabel', font=('Helvetica', 14))
            self.style.configure('main_window_statusbar.TLabel', font=('Helvetica', 9))

    def setup_window_styles(self) -> None:
        if self._is_mac:
            self.style.configure('setup_window_top_label.TLabel', font=('Helvetica', 15))
            self.style.configure('setup_window_output_message_label.TLabel', font=('Helvetica', 15))

            # AWS
            self.style.configure('aws_heading_label.TLabel', font=('Helvetica', 15, 'bold', 'underline'))
            self.style.configure('access_key_id_label.TLabel', font=('Helvetica', 15))
            self.style.configure('aws_secret_key_label.TLabel', font=('Helvetica', 15))
            self.style.configure('region_name_label.TLabel', font=('Helvetica', 15))

            # FFMPEG
            self.style.configure('ffmpeg_heading_label.TLabel', font=('Helvetica', 15, 'bold', 'underline'))
            self.style.configure('ffmpeg_input_label.TLabel', font=('Helvetica', 15))
            self.style.configure('converted_file_suffix_label.TLabel', font=('Helvetica', 15))
            self.style.configure('ffmpeg_example_label.TLabel', font=('Helvetica', 13))

        if self._is_window:
            self.style.configure('setup_window_top_label.TLabel', font=('Helvetica', 15))
            self.style.configure('setup_window_output_message_label.TLabel', font=('Helvetica', 15))

            # AWS
            self.style.configure('aws_heading_label.TLabel', font=('Helvetica', 15, 'bold', 'underline'))
            self.style.configure('access_key_id_label.TLabel', font=('Helvetica', 15))
            self.style.configure('aws_secret_key_label.TLabel', font=('Helvetica', 15))
            self.style.configure('region_name_label.TLabel', font=('Helvetica', 15))

            # FFMPEG
            self.style.configure('ffmpeg_heading_label.TLabel', font=('Helvetica', 15, 'bold', 'underline'))
            self.style.configure('ffmpeg_input_label.TLabel', font=('Helvetica', 15))
            self.style.configure('converted_file_suffix_label.TLabel', font=('Helvetica', 15))
            self.style.configure('ffmpeg_example_label.TLabel', font=('Helvetica', 13))

    def update_database_styles(self) -> None:
        if self._is_mac:
            self.style.configure('update_db_top_label.TLabel', font=('Helvetica', 18, 'underline'))
            self.style.configure('explanation_text_label.TLabel', font=('Helvetica', 15))

        if self._is_window:
            self.style.configure('update_db_top_label.TLabel', font=('Helvetica', 18, 'underline'))
            self.style.configure('explanation_text_label.TLabel', font=('Helvetica', 15))
