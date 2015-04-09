from models.imagedata import ImageData

from bs4 import BeautifulSoup
import time
import requests

'''
The implementation which is actually responsible for fetching the HTML from DeviantArt and turning
it into ImageData objects.
'''
class ScrapeImplementation:
    def __init__(self):
        self.URL = "http://www.deviantart.com/browse/all/"
        self.THUMBNAIL_CLASS = "thumb"
    '''
    Perform the scrape. This does not need to handle de-duplication of ImageData between calls.

    @return a list of ImageData objects.
    '''
    def scrape(self):
        html_doc = requests.get(self.URL).text
        soup = BeautifulSoup(html_doc)
        thumbnails = soup.find("a", {"class": self.THUMBNAIL_CLASS})
        return thumbnails
