"""
Script to create the executable application on Windows and Mac.

Usage:
    - python3.9 setup.py COMMAND
        - Multiple commands can be used.

Commands:
    - clean                 -  Remove `build`, `dist`, `__pycache__` folder and content.
    - clean --full-clean    -  Remove everything that `clean` removes plus `distribution`, `logs`, and `db.sqlite3` folders and files.
    - create                -  Build the application.
                                - Creates ZIP and MSI files if running on Windows
                                - Creates .app bundle and DMG file if running on Mac.
    - distribute            -  Move the created application files that were created with the `create` command to a `distribution` folder.

Example:
    - python3.9 setup.py clean --full-clean create distributes
        - This command would run each command one after the other.
"""

import os
import sys
import shutil
import zipfile
import platform
import cx_Freeze
import subprocess
import distutils.core
from setuptools import find_packages
from typing import Any, Dict, List

from config import APP_TITLE, APP_VERSION


WINDOWS = sys.platform.startswith('win32')
MAC = sys.platform.startswith('darwin')

DMG_NAME = f"{APP_TITLE} Installer"

BUILD_DIR = os.path.join(os.getcwd(), 'build')
DIST_DIR = os.path.join(os.getcwd(), 'dist')
LOGS_DIR = os.path.join(os.getcwd(), 'logs')
FINAL_DISTRIBUTION_DIR = os.path.join(os.getcwd(), 'distribution')

DIST_NAME = f'{APP_TITLE.replace(" ", "_")}-{APP_VERSION}-{platform.system().lower()}_{platform.machine().lower()}'
DIST_PATH = os.path.join(BUILD_DIR, DIST_NAME)

PACKAGES = [
    'botocore',
    'boto3',
    'ffmpeg',
    'pexpect',
    'requests',
    'dotenv',
]
if WINDOWS:
    PACKAGES.append('html')

# pip packages used in setup()
requirements_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'requirements.txt')
INSTALL_REQUIRES = [line.strip() for line in open(requirements_file, 'r')]

ICON = None
BASE = None
EXEC_NAME = None
UPGRADE_CODE = None
PRODUCT_CODE = None

COMMANDS: Dict[str, Any] = dict()


if WINDOWS:
    import msilib
    from cx_Freeze import setup

    BASE = 'Win32GUI'
    EXEC_NAME = f'{APP_TITLE}.exe'
    UPGRADE_CODE = '{6ADD4904-6A36-4D2F-BF96-8241B3D8D474}'
    PRODUCT_CODE = msilib.gen_uuid()  # type:ignore
    ICON = os.path.join(os.getcwd(), 'S3_File_Uploader', 'UI', 'images', 'logo.ico')

if MAC:
    from setuptools import setup

    ICON = os.path.join(os.getcwd(), 'S3_File_Uploader', 'UI', 'images', 'icon.icns')


class Clean(distutils.core.Command):
    """
    Custom clean command to tidy up the project root before creating a new distribution package.
    """
    user_options: List[Any] = [('full-clean', None, 'remove distribution, logs, and database file')]

    def initialize_options(self) -> None:
        """
        Initialize command options.
        """
        self.full_clean = None

        self.pycache_directories = [
            os.path.join(os.getcwd(), 'S3_File_Uploader', '__pycache__'),
            os.path.join(os.getcwd(), 'S3_File_Uploader', 'UI', '__pycache__')
        ]

    def finalize_options(self) -> None:
        """
        Finalize command options.
        """
        pass

    def run(self) -> None:
        """
        Command execution.
        """
        if os.path.exists(BUILD_DIR):
            shutil.rmtree(BUILD_DIR)

        if os.path.exists(DIST_DIR):
            shutil.rmtree(DIST_DIR)

        for dir in self.pycache_directories:
            if os.path.exists(dir):
                shutil.rmtree(dir)

        if self.full_clean:
            if os.path.exists(FINAL_DISTRIBUTION_DIR):
                shutil.rmtree(FINAL_DISTRIBUTION_DIR)

            if os.path.exists(LOGS_DIR):
                shutil.rmtree(LOGS_DIR)

            if os.path.exists(os.path.join(os.getcwd(), 'db.sqlite3')):
                os.remove(os.path.join(os.getcwd(), 'db.sqlite3'))


COMMANDS['clean'] = Clean


class Create(distutils.core.Command):
    user_options: List[Any] = []

    def initialize_options(self) -> None:
        pass

    def finalize_options(self) -> None:
        pass

    if WINDOWS:
        def run(self) -> None:
            self.run_command('bdist_msi')

    if MAC:
        def run(self) -> None:
            self.run_command('py2app')
            self.execute(self.create_application_folder_shortcut, ())
            self.execute(self.create_dmg, ())
            self.execute(self.remove_application_folder_shortcut, ())

        def create_application_folder_shortcut(self) -> None:
            out_code = subprocess.run(['ln', '-s', '/Applications', f'{DIST_DIR}'])

            if out_code.returncode == 0:
                print("Applications folder shortcut created.")
            else:
                print("ERROR: Was not able to create Applications folder shortcut")

        def create_dmg(self) -> None:
            out_code = subprocess.run(
                ['hdiutil', 'create', f'{DIST_DIR}/{DMG_NAME}.dmg',
                 '-ov', '-volname', f'"{DMG_NAME}"', '-fs', 'HFS+', '-srcfolder',
                 f'{DIST_DIR}/']
            )

            if out_code.returncode != 0:
                print("ERROR: Was not able to create dmg.")

        def remove_application_folder_shortcut(self) -> None:
            os.remove(os.path.join(DIST_DIR, 'Applications'))


COMMANDS['create'] = Create

if WINDOWS:
    class BuildExe(cx_Freeze.build_exe):
        def initialize_options(self) -> None:
            self.dist_dir = None
            super().initialize_options()

        def finalize_options(self) -> None:
            if self.dist_dir is None:
                self.dist_dir = self.build_exe
            super().finalize_options()

        def run(self) -> None:
            super().run()
            self.execute(self.make_dist_folder, ())
            self.execute(self.make_zip, ())

        def make_dist_folder(self) -> None:
            """ Make dist folder to add distribution files to. """
            if not os.path.exists(DIST_DIR):
                os.mkdir(DIST_DIR)

        def make_zip(self) -> None:
            """ Create ZIP distribution. """
            self.zip_path = os.path.join(DIST_DIR, f'{DIST_NAME}.zip')
            with zipfile.ZipFile(self.zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for dirpath, dirnames, filenames in os.walk(os.path.join(os.getcwd(), self.build_exe)):
                    for file in filenames:
                        path = os.path.join(os.getcwd(), dirpath, file)
                        arcname = os.path.relpath(path, self.build_exe)
                        zipf.write(path, arcname)

    class BuildMsi(cx_Freeze.bdist_msi):
        def initialize_options(self) -> None:
            super().initialize_options()
            self.target_name = DIST_NAME + '.msi'

        def finalize_options(self) -> None:
            super().finalize_options()

        def run(self) -> None:
            super().run()

    COMMANDS['build_exe'] = BuildExe
    COMMANDS['bdist_msi'] = BuildMsi
    COMMANDS['create'] = Create


class Distribute(distutils.core.Command):
    user_options: List[Any] = []

    def _make_app_bundle_to_zip(self) -> None:
        from zipfile import ZipFile

        if MAC:
            app_bundle_path = os.path.join(DIST_DIR, APP_TITLE + '.app')

            with ZipFile(f'{app_bundle_path}.zip', 'w') as zipObj:
                for folderName, subfolders, filenames in os.walk(app_bundle_path):
                    for filename in filenames:
                        filePath = os.path.join(folderName, filename)
                        zipObj.write(filePath, os.path.basename(filePath))

    def initialize_options(self) -> None:
        if not os.path.exists(FINAL_DISTRIBUTION_DIR):
            os.mkdir(FINAL_DISTRIBUTION_DIR)

        if MAC:
            self._make_app_bundle_to_zip()

            self.dist_package_path = [
                os.path.join(DIST_DIR, APP_TITLE + '.app.zip'),
                os.path.join(DIST_DIR, DMG_NAME + '.dmg')
            ]

        if WINDOWS:
            self.dist_package_path = [
                os.path.join(DIST_DIR, DIST_NAME + '.msi'),
                os.path.join(DIST_DIR, DIST_NAME + '.zip')
            ]

    def finalize_options(self) -> None:
        pass

    def run(self) -> None:
        for path in self.dist_package_path:
            try:
                shutil.copy(path, FINAL_DISTRIBUTION_DIR)
            except:
                os.rmdir(FINAL_DISTRIBUTION_DIR)
                shutil.copytree(path[:path.rfind('/')], FINAL_DISTRIBUTION_DIR)


COMMANDS['distribute'] = Distribute


if WINDOWS:
    extra_options = dict(
        options={
            'build_exe': {
                'packages': PACKAGES,
                'includes': PACKAGES,
                'include_files': [
                    ('S3_File_Uploader', 'S3_File_Uploader')
                ]
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
                'S3_File_Uploader/main.py',
                targetName=EXEC_NAME,
                # pexpect doesn't work on win32gui applications so for now until a different solution
                #   is found need to make the application a console app by commenting out base=BASE
                # base=BASE,
                icon=ICON
            )
        ]
    )

if MAC:
    extra_options = dict(
        app=['S3_File_Uploader/main.py'],
        options={
            'py2app': {
                # Uncomment if needing
                # 'graph': True,

                'iconfile': ICON,
                'emulate_shell_environment': True,
                'argv_emulation': False,
                'extension': '.app',
                'site_packages': True,
                'resources': [
                    'S3_File_Uploader/UI/images'
                ],
                # Any package that is not part of the standard library
                # that is used as an import, needs to be added here
                'packages': PACKAGES
            }
        },
        setup_requires=['py2app']
    )

setup(
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
    package_data={
        'S3_File_Uploader': ['UI/images/*.*']
    },
    install_requires=[
        'html' if WINDOWS else '',
        *INSTALL_REQUIRES
    ],
    zip_safe=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: MacOS X',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: SQL'
    ],
    **extra_options
)
