'''
Main entrypoint to the application.
'''

from models.imagedata import ImageData 
from deviantart.scraper import Scraper

import signal
import sys

if __name__=="__main__":
    '''
    When we receive a kill signal (Ctrl-C on UNIX system and Ctrl-C or Ctrl-BREAK on Windows),
    stop the scraper.
    '''
    def signal_handler(signal, frame):
        scraper.stop()
        print('You pressed Ctrl+C!')
        sys.exit(0)

    '''
    Callback for when the scraper pulls a new list of images.
    '''
    def callback(image_data_items):
        print image_data_items

    scraper = Scraper(callback, ping_interval=1)

    # Run the scraper.
    scraper.run()

    # Setup the signal handler to wait for the kill signal.
    signal.signal(signal.SIGINT, signal_handler)
    print('Press Ctrl+C')
    signal.pause()
