'''
Main entrypoint to the application.
'''

from models.imagedata import ImageData 
from deviantart.scraper import Scraper

import signal
import sys

if __name__=="__main__":
    '''
    Callback for when the scraper pulls a new list of images.
    '''
    def callback(image_data_items):
        print image_data_items


    # Create a scraper.
    scraper = Scraper(callback, ping_interval=1)

    # Run the scraper.
    scraper.run()

    print "Type any value (and enter) to quit"
    val = raw_input()
    scraper.stop()
