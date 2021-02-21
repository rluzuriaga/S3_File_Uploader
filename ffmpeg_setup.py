"""
Python file to download the latest release version of ffmpeg and ffprobe for Windows
and Mac and set it to a bin directory so that it can be added to path.
"""
import os
import sys
import zipfile

import requests
from bs4 import BeautifulSoup

if 'win32' in sys.platform:
    from shutil import move

    web = requests.get("https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-github")

    soup = BeautifulSoup(web.content, 'html.parser')

    download_link = "https://github.com"

    for a_tags in soup.find_all('a'):
        if '-full_build.zip' in a_tags.get('href'):
            download_link += a_tags.get('href')

    ffmpeg_download_file = requests.get(download_link)

    open(os.path.join(os.getcwd(), 'ffmpeg.zip'), 'wb').write(ffmpeg_download_file.content)

    with zipfile.ZipFile(os.path.join(os.getcwd(), 'ffmpeg.zip'), 'r') as zip_ref:
        zip_ref.extractall(os.getcwd())

    bin_path = ""
    for dirpath, dirs, files in os.walk(os.getcwd()):
        if 'bin' in dirs:
            bin_path = os.path.join(dirpath, 'bin')

    move(bin_path, os.getcwd())


if 'darwin' in sys.platform:
    import subprocess

    if not os.path.exists(os.path.join(os.getcwd(), 'bin')):
        os.mkdir(os.path.join(os.getcwd(), 'bin'))

    mac_ffmpeg_info = requests.get('https://evermeet.cx/ffmpeg/info').json()

    mac_download_links = []

    for release in mac_ffmpeg_info:
        if release['name'] in ['ffmpeg', 'ffprobe'] and release['type'] == 'release':
            mac_download_links.append(release['download']['zip']['url'])

    for link in mac_download_links:
        name = 'ffprobe' if 'ffprobe' in link else 'ffmpeg'
        ff_download = requests.get(link)

        open(os.path.join(os.getcwd(), name + '.zip'), 'wb').write(ff_download.content)

        with zipfile.ZipFile(os.path.join(os.getcwd(), name + '.zip'), 'r') as zip_ref:
            zip_ref.extractall(os.path.join(os.getcwd(), 'bin'))

        subprocess.call(['chmod', 'u+x', f'{os.path.join(os.getcwd(), "bin", name)}'])
