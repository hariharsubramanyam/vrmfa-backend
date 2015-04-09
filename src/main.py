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

    # Create the scraper, the callback is currently a function that does nothing.
    #TODO(Harihar): The callback should write the ImageData to a database.
    scraper = Scraper(lambda x: x, ping_interval=1)

    # Run the scraper.
    scraper.run()

    # Setup the signal handler to wait for the kill signal.
    signal.signal(signal.SIGINT, signal_handler)
    print('Press Ctrl+C')
    signal.pause()
