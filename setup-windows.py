from setuptools import find_packages
import cx_Freeze as cx

from S3_File_Uploader import APP_TITLE, APP_VERSION

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
            targetName='S3 File Uploader'
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
        # 'bdist_msi': {
        #     'upgrade_code': '{XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX}',
        # TODO: Check https://cx-freeze.readthedocs.io/en/latest/distutils.html#bdist-msi to see how to implement this
        # }
    }
)
