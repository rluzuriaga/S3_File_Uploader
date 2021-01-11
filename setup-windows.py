import msilib
from setuptools import find_packages
import cx_Freeze as cx

from S3_File_Uploader import APP_TITLE, APP_VERSION

UPGRADE_CODE = '{6ADD4904-6A36-4D2F-BF96-8241B3D8D474}'
PRODUCT_CODE = msilib.gen_uuid()

cx.setup(
    name=APP_TITLE,
    version=APP_VERSION,
    license='MIT',
    url='https://github.com/rluzuriaga/S3_File_Uploader',
    author="Rodrigo Luzuriaga",
    author_email='me@rodrigoluzuriaga.com',
    maintainer='Rodrigo Luzuriaga',
    maintainer_email='me@rodrigoluzuriaga.com',
    packages=find_packages(),
    install_requires=[
        'botocore',
        'boto3',
        'ffmpeg-python',
        'pexpect',
        'requests',
        'html'
    ],
    package_data={
        'S3_File_Uploader': ['UI/images/*.*']
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Win32 (MS Windows)',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: SQL'
    ],
    executables=[
        cx.Executable(
            'S3_File_Uploader/main.py',
            targetName='S3 File Uploader',
            # Comment out the `base="Win32GUI"` line to create a debug msi install.
            # The debug install would run the program opening a command prompt too.
            base="Win32GUI",
            icon="S3_File_Uploader/UI/images/logo.ico"
        )
    ],
    options={
        'build_exe': {
            'packages': [
                'botocore',
                'boto3',
                'ffmpeg',
                'pexpect',
                'requests',
                'html'
            ],
            'includes': [
                'botocore',
                'boto3',
                'ffmpeg',
                'pexpect',
                'requests',
                'html'
            ],
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
    }
)
