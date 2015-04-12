from deviantart.scrape import ScrapeImplementation

import time

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

        # Create the implementation object which performs the scraping.
        self.scrape_implementation = ScrapeImplementation()

    '''
    The loop that will scrape periodically.
    '''
    def run(self):
        self.ticks_until_next_scrape = self.ping_interval
        while True:
            self.ticks_until_next_scrape -= 1
            if self.ticks_until_next_scrape <= 0:
                # Scrape the images and trigger the callback.
                try:
                    images_data_items = self.scrape_implementation.scrape()
                    self.callback(images_data_items)
                except:
                    pass
                self.ticks_until_next_scrape = self.ping_interval
            time.sleep(1)

    '''
    Return string representation of this object.
    '''
    def __repr__(self):
        return "Scraper(ping_interval=%d)" % (self.ping_interval,)
