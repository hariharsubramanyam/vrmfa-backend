from deviantart.scrape import ScrapeImplementation

import time
import threading

'''
The web scraper which pulls image data from DeviantArt.
'''
class Scraper:
    '''
    Create the scraper.

    @param callback - The function to execute after each chunk of image data has been retrieved. 
                      The callback should accept a list of ImageData instances. The scraper does
                      not handle de-duplication, so the callback should.
    @param ping_interval - The number of seconds to wait before pinging the website again.
    '''
    def __init__(self, callback, ping_interval=25):
        self.callback = callback
        self.ping_interval = ping_interval

        # The thread event indicating that the scrape loop should stop.
        self.stop_event = threading.Event()

        # Create the implementation object which performs the scraping.
        self.scrape_implementation = ScrapeImplementation()

        # The thread running the loop for the scraper.
        self.thread = threading.Thread(target=self.scrape_loop, args=[self.stop_event, self.ping_interval, self.callback, self.scrape_implementation])

    '''
    The loop that will scrape periodically.
    '''
    def scrape_loop(self, stop_event, ping_interval, callback, scrape_implementation):
        ticks_until_next_scrape = ping_interval
        while not stop_event.is_set():
            ticks_until_next_scrape -= 1
            if ticks_until_next_scrape <= 0:
                # Scrape the images and trigger the callback.
                images_data_items = scrape_implementation.scrape()
                callback(images_data_items)
                ticks_until_next_scrape = ping_interval
            time.sleep(1)

    '''
    Run the scraper. This will launch another thread, so make sure to terminate it by calling
    stop().
    '''
    def run(self):
        self.stop_event.set()
        self.stop_event.clear()
        self.thread.start()

    '''
    Kill the scraper, if it is currently running.
    '''
    def stop(self):
        self.stop_event.set()

    '''
    Return string representation of this object.
    '''
    def __repr__(self):
        return "Scraper(ping_interval=%d)" % (self.ping_interval,)
