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
        self.FULL_IMG_ATTR = "data-super-full-img"
        self.IMG_ATTR = "data-full-img"
    '''
    Perform the scrape. This does not need to handle de-duplication of ImageData between calls.

    @return a list of ImageData objects.
    '''
    def scrape(self):
        # Get the HTML.
        html_doc = requests.get(self.URL).text

        # Create the soup object for extracting tags and stuff.
        soup = BeautifulSoup(html_doc)

        # Find all the thumbnail images.
        thumbnails = soup.find_all("a", {"class": self.THUMBNAIL_CLASS})

        image_data_items = []
        for thumbnail in thumbnails:
            if thumbnail.has_attr(self.FULL_IMG_ATTR):
                image_data_items.append(ImageData(thumbnail[self.FULL_IMG_ATTR]))
            elif thumbnail.has_attr(self.IMG_ATTR):
                image_data_items.append(ImageData(thumbnail[self.IMG_ATTR]))
        return image_data_items
