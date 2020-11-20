"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup, find_packages

APP = ['S3_File_Uploader/main.py']
DATA_FILES = []
OPTIONS = {
    'resources': [
        'S3_File_Uploader/UI/images'
    ]
}

setup(
    name='S3 File Uploader',
    app=APP,
    packages=find_packages(),
    data_files=DATA_FILES,
    package_data={
        'S3_File_Uploader': ['UI/images/*.*']
    },
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    install_requires=[
        'boto3',
        'botocore',
        'ffmpeg-python',
        'pexpect'
    ],
    zip_safe=False,
)
