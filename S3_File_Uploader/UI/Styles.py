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

        self.label_styles()

    def label_styles(self) -> None:
        if self._is_mac:
            # All UI
            self.style.configure('regular.TButton', font=('Helvetica', 15))
            self.style.configure('regular.TCheckbutton', font=('Helvetica', 15))

            # MainWindow.py
            self.style.configure('main_window_top_label.TLabel', font=('Helvetica', 15))
            self.style.configure('main_window_statusbar.TLabel', font=('Helvetica', 10))

        if self._is_window:
            # All UI
            self.style.configure('regular.TButton', font=('Helvetica', 12))
            self.style.configure('regular.TCheckbutton', font=('Helvetica', 12))

            # MainWindow.py
            self.style.configure('main_window_top_label.TLabel', font=('Helvetica', 14))
            self.style.configure('main_window_statusbar.TLabel', font=('Helvetica', 9))
