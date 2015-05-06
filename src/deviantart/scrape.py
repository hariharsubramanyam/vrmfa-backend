from imagedata import ImageData

from bs4 import BeautifulSoup
import random
import time
import requests

'''
The implementation which is actually responsible for fetching the HTML from DeviantArt and turning
it into ImageData objects.
'''
class ScrapeImplementation:
    def __init__(self):
        self.UPPER_BOUND = 40000
        self.URL = "http://www.deviantart.com/browse/all/"
        self.THUMBNAIL_CLASS = "thumb"
        self.FULL_IMG_ATTR = "data-super-full-img"
        self.IMG_ATTR = "data-full-img"
    '''
    Perform the scrape. This does not need to handle de-duplication of ImageData between calls.

    @return a list of ImageData objects.
    '''
    def scrape(self):
        # Get the HTML from a random page.
        page_offset = str(random.randint(0, self.UPPER_BOUND))
        html_doc = requests.get(self.URL + "?offset=" + page_offset).text

        # Create the soup object for extracting tags and stuff.
        soup = BeautifulSoup(html_doc)

        # Find all the thumbnail images.
        thumbnails = soup.find_all("a", {"class": self.THUMBNAIL_CLASS})

        image_data_items = []
        for thumbnail in thumbnails:
            if not thumbnail.img.has_attr("alt"):
                continue
            descr = thumbnail.img["alt"]
           # if thumbnail.has_attr(self.FULL_IMG_ATTR):
           #     image_data_items.append(ImageData(thumbnail[self.FULL_IMG_ATTR], descr))
            #if thumbnail.has_attr(self.IMG_ATTR):
            #    image_data_items.append(ImageData(thumbnail[self.IMG_ATTR], descr))
            #else:
            image_data_items.append(ImageData(thumbnail.img["src"], descr))
        return image_data_items
