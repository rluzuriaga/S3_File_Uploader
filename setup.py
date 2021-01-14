import os
import sys
import zipfile
import platform
import cx_Freeze
import distutils.core
from shutil import rmtree, copy
from setuptools import find_packages

from S3_File_Uploader import APP_TITLE, APP_VERSION


WINDOWS = sys.platform.startswith('win32')
MAC = sys.platform.startswith('darwin')

BUILD_DIR = os.path.join(os.getcwd(), 'build')
DIST_DIR = os.path.join(os.getcwd(), 'dist')
LOGS_DIR = os.path.join(os.getcwd(), 'logs')
FINAL_DISTRIBUTION_DIR = os.path.join(os.getcwd(), 'distribution')

DIST_NAME = f'{APP_TITLE.replace(" ", "_")}-{APP_VERSION}-{platform.system().lower()}_{platform.machine().lower()}'
DIST_PATH = os.path.join(BUILD_DIR, DIST_NAME)
EXEC_ICON = os.path.join(os.getcwd(), 'S3_File_Uploader', 'UI', 'images', 'logo.ico')
EXEC_BASE = None
EXEC_NAME = None
UPGRADE_CODE = None
PRODUCT_CODE = None

if WINDOWS:
    import msilib

    EXEC_BASE = 'Win32GUI'
    EXEC_NAME = f'{APP_TITLE}.exe'
    UPGRADE_CODE = '{6ADD4904-6A36-4D2F-BF96-8241B3D8D474}'
    PRODUCT_CODE = msilib.gen_uuid()

if MAC:
    EXEC_NAME = APP_TITLE


class Clean(distutils.core.Command):
    """
    Custom clean command to tidy up the project root before creating a new distribution package.
    """
    user_options = [('full-clean', None, 'remove distribution, logs, and database file')]

    def initialize_options(self):
        """
        Initialize command options.
        """
        self.full_clean = None

        self.pycache_directories = [
            os.path.join(os.getcwd(), 'S3_File_Uploader', '__pycache__'),
            os.path.join(os.getcwd(), 'S3_File_Uploader', 'UI', '__pycache__')
        ]

    def finalize_options(self):
        """
        Finalize command options.
        """
        pass

    def run(self):
        """
        Command execution.
        """
        if os.path.exists(BUILD_DIR):
            rmtree(BUILD_DIR)

        if os.path.exists(DIST_DIR):
            rmtree(DIST_DIR)

        for dir in self.pycache_directories:
            if os.path.exists(dir):
                rmtree(dir)

        if self.full_clean:
            if os.path.exists(FINAL_DISTRIBUTION_DIR):
                rmtree(FINAL_DISTRIBUTION_DIR)

            if os.path.exists(LOGS_DIR):
                rmtree(LOGS_DIR)

            if os.path.exists(os.path.join(os.getcwd(), 'db.sqlite3')):
                os.remove(os.path.join(os.getcwd(), 'db.sqlite3'))


class BuildMsi(cx_Freeze.bdist_msi):
    def initialize_options(self):
        super().initialize_options()
        self.target_name = DIST_NAME + '.msi'

        if not os.path.exists(FINAL_DISTRIBUTION_DIR):
            os.mkdir(FINAL_DISTRIBUTION_DIR)

    def finalize_options(self):
        super().finalize_options()

    def run(self):
        super().run()
        self.execute(self.copy_to_final_distribute_folder, ())

    def copy_to_final_distribute_folder(self):
        if os.path.exists(os.path.join(DIST_DIR, DIST_NAME + '.msi')):
            copy(os.path.join(DIST_DIR, DIST_NAME + '.msi'), FINAL_DISTRIBUTION_DIR)


class BuildExe(cx_Freeze.build_exe):
    def initialize_options(self):
        self.dist_dir = None
        super().initialize_options()

        if not os.path.exists(FINAL_DISTRIBUTION_DIR):
            os.mkdir(FINAL_DISTRIBUTION_DIR)

    def finalize_options(self):
        if self.dist_dir is None:
            self.dist_dir = self.build_exe
        super().finalize_options()

    def run(self):
        super().run()
        self.execute(self.make_dist_folder, ())
        self.execute(self.make_zip, ())
        self.execute(self.copy_to_final_distribute_folder, ())

    def make_dist_folder(self):
        """ Make dist folder to add distribution files to. """
        if not os.path.exists(DIST_DIR):
            os.mkdir(DIST_DIR)

    def make_zip(self):
        """ Create ZIP distribution. """
        self.zip_path = os.path.join(DIST_DIR, f'{DIST_NAME}.zip')
        with zipfile.ZipFile(self.zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for dirpath, dirnames, filenames in os.walk(os.path.join(os.getcwd(), self.build_exe)):
                for file in filenames:
                    path = os.path.join(os.getcwd(), dirpath, file)
                    arcname = os.path.relpath(path, self.build_exe)
                    zipf.write(path, arcname)

    def copy_to_final_distribute_folder(self):
        if os.path.exists(self.zip_path):
            copy(self.zip_path, FINAL_DISTRIBUTION_DIR)


COMMANDS = {
    'clean': Clean,
    'bdist_msi': BuildMsi,
    'build_exe': BuildExe
}

PACKAGES = [
    'botocore',
    'boto3',
    'ffmpeg',
    'pexpect',
    'requests',
    'html'
]

INCLUDES = [
    'botocore',
    'boto3',
    'ffmpeg',
    'pexpect',
    'requests',
    'html'
]

INCLUDE_FILES = [
    ('S3_File_Uploader', 'S3_File_Uploader')
]


cx_Freeze.setup(
    cmdclass=COMMANDS,
    name=APP_TITLE,
    version=APP_VERSION,
    license='MIT',
    url='https://github.com/rluzuriaga/S3_File_Uploader',
    author="Rodrigo Luzuriaga",
    author_email='me@rodrigoluzuriaga.com',
    maintainer='Rodrigo Luzuriaga',
    maintainer_email='me@rodrigoluzuriaga.com',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: SQL',
        'Topic :: Utilities'
    ],

    options={
        'build_exe': {
            'packages': PACKAGES,
            'includes': INCLUDES,
            'include_files': INCLUDE_FILES
        },
        'bdist_msi': {
            'upgrade_code': UPGRADE_CODE,
            'all_users': False,
            'product_code': PRODUCT_CODE,

            # https://stackoverflow.com/questions/15734703/use-cx-freeze-to-create-an-msi-that-adds-a-shortcut-to-the-desktop#15736406
            'data': {
                'Shortcut': [
                    (
                        "DesktopShortcut",                  # Shortcut
                        "DesktopFolder",                    # Directory_
                        "S3 File Uploader",                 # Name
                        "TARGETDIR",                        # Component_
                        "[TARGETDIR]S3 File Uploader.exe",  # Target
                        None,                               # Arguments
                        None,                               # Description
                        None,                               # Hotkey
                        None,                               # Icon
                        None,                               # IconIndex
                        None,                               # ShowCmd
                        "TARGETDIR"                         # WkDir
                    ),
                    (
                        "MenuShortcut",                     # Shortcut
                        "ProgramMenuFolder",                # Directory_
                        "S3 File Uploader",                 # Name
                        "TARGETDIR",                        # Component_
                        "[TARGETDIR]S3 File Uploader.exe",  # Target
                        None,                               # Arguments
                        None,                               # Description
                        None,                               # Hotkey
                        None,                               # Icon
                        None,                               # IconIndex
                        None,                               # ShowCmd
                        "TARGETDIR"                         # WkDir
                    )
                ]
            }
        }
    },

    executables=[
        cx_Freeze.Executable(
            script='S3_File_Uploader/main.py',
            targetName=EXEC_NAME,
            base=EXEC_BASE,
            icon=EXEC_ICON
        )
    ],
)
