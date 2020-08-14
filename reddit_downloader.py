import os
from tqdm import tqdm
import requests
import config


class GetUrls:
    def __init__(self, filename):
        self.filename = filename
        self.raw_urls = []
        self.image_urls = []

    def get_file(self):
        # Gets filename and opens file
        file1 = open(self.filename, 'r')
        # Takes file and gets individual lines as list
        Lines = file1.readlines()
        # Returns list of lines
        return Lines

    def parse_urls(self):
        Lines = self.get_file()
        # Iterates through lines checking if element is in the line
        for line in Lines:
            if config.element in line:
                # Gets parts of line
                parts = line.split(' ')
                for part in parts:
                    # Checks for image url
                    if part[:24] == 'href="https://i.redd.it/':
                        self.raw_urls.append(part)


    # Gets actual urls from url lines
    def extract_url(self):
        for url in self.raw_urls:
            self.image_urls.append(url[6:-1])


class Setup:
    def __init__(self, directory):
        self.directory = directory

    # Check if directory exists
    def check_dir(self):
        return os.path.isdir(self.directory)

    # Makes a directory if none exists
    def setup(self):
        if not self.check_dir():
            os.mkdir(self.directory)


class DownloadUrls:
    def __init__(self, urls, directory):
        self.urls = urls
        self.path = directory

    # Pases all image urls to download_image
    def download(self):
        for image in self.urls:
            self.download_image(image)

    # Downloads url to directory using requests and stream
    def download_image(self, url):
        local_filename = url.split("/")[-1]
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(f"{self.path}/{local_filename}", "wb+") as f:
                for chunk in tqdm(r.iter_content(chunk_size=8192)):
                    if chunk:
                        f.write(chunk)


if __name__ == "__main__":
    FILENAME = config.filename
    DIRECTORY = config.directory

    geturls = GetUrls(FILENAME)
    geturls.parse_urls()
    geturls.extract_url()
    urls = geturls.image_urls

    _setup = Setup(DIRECTORY)
    _setup.setup()

    _dowload = DownloadUrls(urls, DIRECTORY)
    _dowload.download()
